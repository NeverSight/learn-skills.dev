---
name: mapbox-mcp-runtime-patterns
description: Integration patterns for Mapbox MCP Server in AI applications and agent frameworks. Covers runtime integration with pydantic-ai, mastra, LangChain, and custom agents. Use when building AI-powered applications that need geospatial capabilities.
---

# Mapbox MCP Runtime Patterns

This skill provides patterns for integrating the Mapbox MCP Server into AI applications for production use with geospatial capabilities.

## What is Mapbox MCP Server?

The [Mapbox MCP Server](https://github.com/mapbox/mcp-server) is a Model Context Protocol (MCP) server that provides AI agents with geospatial tools:

**Offline Tools (Turf.js):**

- Distance, bearing, midpoint calculations
- Point-in-polygon tests
- Area, buffer, centroid operations
- Bounding box, geometry simplification
- No API calls, instant results

**Mapbox API Tools:**

- Directions and routing
- Reverse geocoding
- POI category search
- Isochrones (reachability)
- Travel time matrices
- Static map images
- GPS trace map matching
- Multi-stop route optimization

**Utility Tools:**

- Server version info
- POI category list

**Key benefit:** Give your AI application geospatial superpowers without manually integrating multiple APIs.

## Understanding Tool Categories

Before integrating, understand the key distinctions between tools to help your LLM choose correctly:

### Distance: "As the Crow Flies" vs "Along Roads"

**Straight-line distance** (offline, instant):

- Tools: `distance_tool`, `bearing_tool`, `midpoint_tool`
- Use for: Proximity checks, "how far away is X?", comparing distances
- Example: "Is this restaurant within 2 miles?" → `distance_tool`

**Route distance** (API, traffic-aware):

- Tools: `directions_tool`, `matrix_tool`
- Use for: Navigation, drive time, "how long to drive?"
- Example: "How long to drive there?" → `directions_tool`

### Search: Type vs Specific Place

**Category/type search**:

- Tool: `category_search_tool`
- Use for: "Find coffee shops", "restaurants nearby", browsing by type
- Example: "What hotels are near me?" → `category_search_tool`

**Specific place/address**:

- Tool: `search_and_geocode_tool`, `reverse_geocode_tool`
- Use for: Named places, street addresses, landmarks
- Example: "Find 123 Main Street" → `search_and_geocode_tool`

### Travel Time: Area vs Route

**Reachable area** (what's within reach):

- Tool: `isochrone_tool`
- Returns: GeoJSON polygon of everywhere reachable
- Example: "What can I reach in 15 minutes?" → `isochrone_tool`

**Specific route** (how to get there):

- Tool: `directions_tool`
- Returns: Turn-by-turn directions to one destination
- Example: "How do I get to the airport?" → `directions_tool`

### Cost & Performance

**Offline tools** (free, instant):

- No API calls, no token usage
- Use whenever real-time data not needed
- Examples: `distance_tool`, `point_in_polygon_tool`, `area_tool`

**API tools** (requires token, counts against usage):

- Real-time traffic, live POI data, current conditions
- Use when accuracy and freshness matter
- Examples: `directions_tool`, `category_search_tool`, `isochrone_tool`

**Best practice:** Prefer offline tools when possible, use API tools when you need real-time data or routing.

## Installation & Setup

### Option 1: Hosted Server (Recommended)

**Easiest integration** - Use Mapbox's hosted MCP server at:

```
https://mcp.mapbox.com/mcp
```

No installation required. Simply pass your Mapbox access token in the `Authorization` header.

**Benefits:**

- No server management
- Always up-to-date
- Production-ready
- Lower latency (Mapbox infrastructure)

**Authentication:**

Use token-based authentication (standard for programmatic access):

```
Authorization: Bearer your_mapbox_token
```

**Note:** The hosted server also supports OAuth, but that's primarily for interactive flows (coding assistants, not production apps).

### Option 2: Self-Hosted

For custom deployments or development:

```bash
npm install @mapbox/mcp-server
```

Or use directly via npx:

```bash
npx @mapbox/mcp-server
```

**Environment setup:**

```bash
export MAPBOX_ACCESS_TOKEN="your_token_here"
```

## Integration Patterns

## Python Frameworks

### Pattern 1: Pydantic AI Integration

**Use case:** Building AI agents with type-safe tools in Python

#### Using Hosted Server (Recommended)

> **Common mistake:** When using pydantic-ai with OpenAI, the correct import is `from pydantic_ai.models.openai import OpenAIChatModel`. Do NOT use `OpenAIModel` — that class does not exist in pydantic-ai and will throw an ImportError at runtime.

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
import requests
import json
import os

class MapboxMCP:
    """Mapbox MCP via hosted server."""

    def __init__(self, token: str = None):
        self.url = 'https://mcp.mapbox.com/mcp'
        self.headers = {'Content-Type': 'application/json'}

        # Use token from environment or parameter
        token = token or os.getenv('MAPBOX_ACCESS_TOKEN')
        if token:
            self.headers['Authorization'] = f'Bearer {token}'

    def call_tool(self, tool_name: str, params: dict) -> dict:
        """Call MCP tool via HTTPS."""
        request = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'tools/call',
            'params': {
                'name': tool_name,
                'arguments': params
            }
        }

        response = requests.post(
            self.url,
            headers=self.headers,
            json=request
        )
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            raise RuntimeError(f"MCP error: {data['error']['message']}")

        return data['result']['content'][0]['text']

# Create agent with Mapbox tools
# Pass token directly or set MAPBOX_ACCESS_TOKEN env var
mapbox = MapboxMCP(token='your_token')

agent = Agent(
    model=OpenAIChatModel('gateway/openai:gpt-5.2'),
    tools=[
        lambda from_loc, to_loc: mapbox.call_tool(
            'directions_tool',
            {'coordinates': [from_loc, to_loc], 'routing_profile': 'mapbox/driving-traffic'}
        ),
        lambda address: mapbox.call_tool(
            'reverse_geocode_tool',
            {'coordinates': {'longitude': address[0], 'latitude': address[1]}}
        )
    ]
)

# Use agent
result = agent.run_sync(
    "What's the driving time from Boston to NYC?"
)
```

#### Using Self-Hosted Server

```python
import subprocess

class MapboxMCPLocal:
    def __init__(self, token: str):
        self.token = token
        self.mcp_process = subprocess.Popen(
            ['npx', '@mapbox/mcp-server'],
            env={'MAPBOX_ACCESS_TOKEN': token},
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

    def call_tool(self, tool_name: str, params: dict) -> dict:
        # ... similar to hosted but via subprocess
        pass
```

**Benefits:**

- Type-safe tool definitions
- Seamless MCP integration
- Python-native development

### Pattern 2: CrewAI Integration

**Use case:** Multi-agent orchestration with geospatial capabilities

CrewAI enables building autonomous agent crews with specialized roles. Integration with Mapbox MCP adds geospatial intelligence to your crew.

```python
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
import requests
import os
from typing import Type
from pydantic import BaseModel, Field

class MapboxMCP:
    """Mapbox MCP connector."""

    def __init__(self, token: str = None):
        self.url = 'https://mcp.mapbox.com/mcp'
        token = token or os.getenv('MAPBOX_ACCESS_TOKEN')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    def call_tool(self, tool_name: str, params: dict) -> str:
        request = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'tools/call',
            'params': {'name': tool_name, 'arguments': params}
        }
        response = requests.post(self.url, headers=self.headers, json=request)
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            raise RuntimeError(f"MCP error: {data['error']['message']}")

        return data['result']['content'][0]['text']

# Create Mapbox tools for CrewAI
class DirectionsTool(BaseTool):
    name: str = "directions_tool"
    description: str = "Get driving directions between two locations"

    class InputSchema(BaseModel):
        origin: list = Field(description="Origin [lng, lat]")
        destination: list = Field(description="Destination [lng, lat]")

    args_schema: Type[BaseModel] = InputSchema

    def __init__(self):
        super().__init__()
        self.mcp = MapboxMCP()

    def _run(self, origin: list, destination: list) -> str:
        result = self.mcp.call_tool('directions_tool', {
            'coordinates': [
                {'longitude': origin[0], 'latitude': origin[1]},
                {'longitude': destination[0], 'latitude': destination[1]}
            ],
            'routing_profile': 'mapbox/driving-traffic'
        })
        return f"Directions: {result}"

class GeocodeTool(BaseTool):
    name: str = "reverse_geocode_tool"
    description: str = "Convert coordinates to human-readable address"

    class InputSchema(BaseModel):
        coordinates: list = Field(description="Coordinates [lng, lat]")

    args_schema: Type[BaseModel] = InputSchema

    def __init__(self):
        super().__init__()
        self.mcp = MapboxMCP()

    def _run(self, coordinates: list) -> str:
        result = self.mcp.call_tool('reverse_geocode_tool', {
            'coordinates': {'longitude': coordinates[0], 'latitude': coordinates[1]}
        })
        return result

class SearchPOITool(BaseTool):
    name: str = "search_poi"
    description: str = "Find points of interest by category near a location"

    class InputSchema(BaseModel):
        category: str = Field(description="POI category (restaurant, hotel, etc.)")
        location: list = Field(description="Search center [lng, lat]")

    args_schema: Type[BaseModel] = InputSchema

    def __init__(self):
        super().__init__()
        self.mcp = MapboxMCP()

    def _run(self, category: str, location: list) -> str:
        result = self.mcp.call_tool('category_search_tool', {
            'category': category,
            'proximity': {'longitude': location[0], 'latitude': location[1]}
        })
        return result

# Create specialized agents with geospatial tools
location_analyst = Agent(
    role='Location Analyst',
    goal='Analyze geographic locations and provide insights',
    backstory="""Expert in geographic analysis and location intelligence.

    Use search_poi for finding types of places (restaurants, hotels).
    Use reverse_geocode_tool for converting coordinates to addresses.""",
    tools=[GeocodeTool(), SearchPOITool()],
    verbose=True
)

route_planner = Agent(
    role='Route Planner',
    goal='Plan optimal routes and provide travel time estimates',
    backstory="""Experienced logistics coordinator specializing in route optimization.

    Use directions_tool for route distance along roads with traffic.
    Always use when traffic-aware travel time is needed.""",
    tools=[DirectionsTool()],
    verbose=True
)

# Create tasks
find_restaurants_task = Task(
    description="""
    Find the top 5 restaurants near coordinates [-73.9857, 40.7484] (Times Square).
    Provide their names and approximate distances.
    """,
    agent=location_analyst,
    expected_output="List of 5 restaurants with distances"
)

plan_route_task = Task(
    description="""
    Plan a route from [-74.0060, 40.7128] (downtown NYC) to [-73.9857, 40.7484] (Times Square).
    Provide driving time considering current traffic.
    """,
    agent=route_planner,
    expected_output="Route with estimated driving time"
)

# Create and run crew
crew = Crew(
    agents=[location_analyst, route_planner],
    tasks=[find_restaurants_task, plan_route_task],
    verbose=True
)

result = crew.kickoff()
print(result)
```

**Real-world example - Restaurant finder crew:**

```python
# Define crew for restaurant recommendation system
class RestaurantCrew:
    def __init__(self):
        self.mcp = MapboxMCP()

        # Location specialist agent
        self.location_agent = Agent(
            role='Location Specialist',
            goal='Find and analyze restaurant locations',
            tools=[SearchPOITool(), GeocodeTool()],
            backstory='Expert in finding the best dining locations'
        )

        # Logistics agent
        self.logistics_agent = Agent(
            role='Logistics Coordinator',
            goal='Calculate travel times and optimal routes',
            tools=[DirectionsTool()],
            backstory='Specialist in urban navigation and time optimization'
        )

    def find_restaurants_with_commute(self, user_location: list, max_minutes: int):
        # Task 1: Find nearby restaurants
        search_task = Task(
            description=f"Find restaurants near {user_location}",
            agent=self.location_agent,
            expected_output="List of restaurants with coordinates"
        )

        # Task 2: Calculate travel times
        route_task = Task(
            description=f"Calculate travel time to each restaurant from {user_location}",
            agent=self.logistics_agent,
            expected_output="Travel times to each restaurant",
            context=[search_task]  # Depends on search results
        )

        crew = Crew(
            agents=[self.location_agent, self.logistics_agent],
            tasks=[search_task, route_task],
            verbose=True
        )

        return crew.kickoff()

# Usage
restaurant_crew = RestaurantCrew()
results = restaurant_crew.find_restaurants_with_commute(
    user_location=[-73.9857, 40.7484],
    max_minutes=15
)
```

**Benefits:**

- Multi-agent orchestration with geospatial tools
- Task dependencies and context passing
- Role-based agent specialization
- Autonomous crew execution

### Pattern 3: Smolagents Integration

**Use case:** Lightweight agents with geospatial capabilities (Hugging Face)

Smolagents is Hugging Face's simple, efficient agent framework. Perfect for deploying geospatial agents with minimal overhead.

```python
from smolagents import CodeAgent, Tool, HfApiModel
import requests
import os

class MapboxMCP:
    """Mapbox MCP connector."""

    def __init__(self, token: str = None):
        self.url = 'https://mcp.mapbox.com/mcp'
        token = token or os.getenv('MAPBOX_ACCESS_TOKEN')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    def call_tool(self, tool_name: str, params: dict) -> str:
        request = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'tools/call',
            'params': {'name': tool_name, 'arguments': params}
        }
        response = requests.post(self.url, headers=self.headers, json=request)
        result = response.json()['result']
        return result['content'][0]['text']

# Create Mapbox tools for Smolagents
class DirectionsTool(Tool):
    name = "directions_tool"
    description = """
    Get driving directions between two locations.

    Args:
        origin: Origin coordinates as [longitude, latitude]
        destination: Destination coordinates as [longitude, latitude]

    Returns:
        Directions with distance and travel time
    """

    def __init__(self):
        super().__init__()
        self.mcp = MapboxMCP()

    def forward(self, origin: list, destination: list) -> str:
        return self.mcp.call_tool('directions_tool', {
            'coordinates': [
                {'longitude': origin[0], 'latitude': origin[1]},
                {'longitude': destination[0], 'latitude': destination[1]}
            ],
            'routing_profile': 'mapbox/driving-traffic'
        })

class CalculateDistanceTool(Tool):
    name = "distance_tool"
    description = """
    Calculate distance between two points (offline, instant).

    Args:
        from_coords: Start coordinates [longitude, latitude]
        to_coords: End coordinates [longitude, latitude]
        units: 'miles' or 'kilometers'

    Returns:
        Distance as a number
    """

    def __init__(self):
        super().__init__()
        self.mcp = MapboxMCP()

    def forward(self, from_coords: list, to_coords: list, units: str = 'miles') -> str:
        return self.mcp.call_tool('distance_tool', {
            'from': {'longitude': from_coords[0], 'latitude': from_coords[1]},
            'to': {'longitude': to_coords[0], 'latitude': to_coords[1]},
            'units': units
        })

class SearchPOITool(Tool):
    name = "search_poi"
    description = """
    Search for points of interest by category.

    Args:
        category: POI category (restaurant, hotel, gas_station, etc.)
        location: Search center [longitude, latitude]

    Returns:
        List of nearby POIs with names and coordinates
    """

    def __init__(self):
        super().__init__()
        self.mcp = MapboxMCP()

    def forward(self, category: str, location: list) -> str:
        return self.mcp.call_tool('category_search_tool', {
            'category': category,
            'proximity': {'longitude': location[0], 'latitude': location[1]}
        })

class IsochroneTool(Tool):
    name = "isochrone_tool"
    description = """
    Calculate reachable area within time limit (isochrone).

    Args:
        location: Center point [longitude, latitude]
        minutes: Time limit in minutes
        profile: 'mapbox/driving', 'mapbox/walking', or 'mapbox/cycling'

    Returns:
        GeoJSON polygon of reachable area
    """

    def __init__(self):
        super().__init__()
        self.mcp = MapboxMCP()

    def forward(self, location: list, minutes: int, profile: str = 'mapbox/driving') -> str:
        return self.mcp.call_tool('isochrone_tool', {
            'coordinates': {'longitude': location[0], 'latitude': location[1]},
            'contours_minutes': [minutes],
            'profile': profile
        })

# Create agent with Mapbox tools
model = HfApiModel()

agent = CodeAgent(
    tools=[
        DirectionsTool(),
        CalculateDistanceTool(),
        SearchPOITool(),
        IsochroneTool()
    ],
    model=model
)

# Use agent
result = agent.run(
    "Find restaurants within 10 minutes walking from Times Square NYC "
    "(coordinates: -73.9857, 40.7484). Calculate distances to each."
)

print(result)
```

**Real-world example - Property search agent:**

```python
class PropertySearchAgent:
    def __init__(self):
        self.mcp = MapboxMCP()

        # Create specialized tools
        tools = [
            IsochroneTool(),
            SearchPOITool(),
            CalculateDistanceTool()
        ]

        self.agent = CodeAgent(
            tools=tools,
            model=HfApiModel()
        )

    def find_properties_near_work(
        self,
        work_location: list,
        max_commute_minutes: int,
        property_locations: list[dict]
    ):
        """Find properties within commute time of work."""

        prompt = f"""
        I need to find properties within {max_commute_minutes} minutes
        driving of my work at {work_location}.

        Property locations to check:
        {property_locations}

        For each property:
        1. Calculate if it's within the commute time
        2. Find nearby amenities (grocery stores, restaurants)
        3. Calculate distances to key locations

        Return a ranked list of properties with commute time and nearby amenities.
        """

        return self.agent.run(prompt)

# Usage
property_agent = PropertySearchAgent()

properties = [
    {'id': 1, 'address': '123 Main St', 'coords': [-122.4194, 37.7749]},
    {'id': 2, 'address': '456 Oak Ave', 'coords': [-122.4094, 37.7849]},
]

results = property_agent.find_properties_near_work(
    work_location=[-122.4, 37.79],  # Downtown SF
    max_commute_minutes=30,
    property_locations=properties
)
```

**Benefits:**

- Lightweight and efficient
- Simple tool definition
- Code-based agent execution
- Great for production deployment

## JavaScript/TypeScript Frameworks

### Pattern 4: Mastra Integration

**Use case:** Building multi-agent systems with geospatial workflows

```typescript
import { Mastra } from '@mastra/core';

class MapboxMCP {
  private url = 'https://mcp.mapbox.com/mcp';
  private headers: Record<string, string>;

  constructor(token?: string) {
    const mapboxToken = token || process.env.MAPBOX_ACCESS_TOKEN;
    this.headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${mapboxToken}`
    };
  }

  async callTool(toolName: string, params: any): Promise<any> {
    const request = {
      jsonrpc: '2.0',
      id: Date.now(),
      method: 'tools/call',
      params: { name: toolName, arguments: params }
    };

    const response = await fetch(this.url, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(request)
    });

    const data = await response.json();
    return JSON.parse(data.result.content[0].text);
  }
}

// Create Mastra agent with Mapbox tools
import { Agent } from '@mastra/core/agent';
import { createTool } from '@mastra/core/tools';
import { z } from 'zod';

const mcp = new MapboxMCP();

// Create Mapbox tools
const searchPOITool = createTool({
  id: 'search-poi',
  description: 'Find places of a specific category near a location',
  inputSchema: z.object({
    category: z.string(),
    location: z.array(z.number()).length(2)
  }),
  execute: async ({ category, location }) => {
    return await mcp.callTool('category_search_tool', {
      category,
      proximity: { longitude: location[0], latitude: location[1] }
    });
  }
});

const getDirectionsTool = createTool({
  id: 'get-directions',
  description: 'Get driving directions with traffic',
  inputSchema: z.object({
    origin: z.array(z.number()).length(2),
    destination: z.array(z.number()).length(2)
  }),
  execute: async ({ origin, destination }) => {
    return await mcp.callTool('directions_tool', {
      coordinates: [
        { longitude: origin[0], latitude: origin[1] },
        { longitude: destination[0], latitude: destination[1] }
      ],
      routing_profile: 'mapbox/driving-traffic'
    });
  }
});

// Create location agent
const locationAgent = new Agent({
  id: 'location-agent',
  name: 'Location Intelligence Agent',
  instructions: 'You help users find places and plan routes with geospatial tools.',
  model: 'openai/gpt-5.2',
  tools: {
    searchPOITool,
    getDirectionsTool
  }
});

// Use agent
const result = await locationAgent.generate([
  { role: 'user', content: 'Find restaurants near Times Square NYC (-73.9857, 40.7484)' }
]);
```

**Benefits:**

- Multi-step geospatial workflows
- Agent orchestration
- State management

### Pattern 5: LangChain Integration

**Use case:** Building conversational AI with geospatial tools

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { AgentExecutor, createToolCallingAgent } from 'langchain/agents';
import { DynamicStructuredTool } from '@langchain/core/tools';
import { ChatPromptTemplate, MessagesPlaceholder } from '@langchain/core/prompts';
import { z } from 'zod';

// MCP Server wrapper for hosted server
class MapboxMCP {
  private url = 'https://mcp.mapbox.com/mcp';
  private headers: Record<string, string>;

  constructor(token?: string) {
    const mapboxToken = token || process.env.MAPBOX_ACCESS_TOKEN;
    this.headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${mapboxToken}`
    };
  }

  async callTool(name: string, args: any): Promise<string> {
    const request = {
      jsonrpc: '2.0',
      id: Date.now(),
      method: 'tools/call',
      params: { name, arguments: args }
    };

    const response = await fetch(this.url, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(request)
    });

    const data = await response.json();
    return data.result.content[0].text;
  }
}

// Create LangChain tools from MCP
const mcp = new MapboxMCP();

const tools = [
  new DynamicStructuredTool({
    name: 'directions_tool',
    description:
      'Get turn-by-turn driving directions with traffic-aware route distance along roads. Use when you need the actual driving route or traffic-aware duration.',
    schema: z.object({
      origin: z.tuple([z.number(), z.number()]).describe('Origin [longitude, latitude]'),
      destination: z.tuple([z.number(), z.number()]).describe('Destination [longitude, latitude]')
    }) as any,
    func: async ({ origin, destination }: any) => {
      return await mcp.callTool('directions_tool', {
        coordinates: [
          { longitude: origin[0], latitude: origin[1] },
          { longitude: destination[0], latitude: destination[1] }
        ],
        routing_profile: 'mapbox/driving-traffic'
      });
    }
  }),

  new DynamicStructuredTool({
    name: 'category_search_tool',
    description:
      'Find ALL places of a specific category type near a location. Use when user wants to browse places by type (restaurants, hotels, coffee, etc.).',
    schema: z.object({
      category: z.string().describe('POI category: restaurant, hotel, coffee, etc.'),
      location: z.tuple([z.number(), z.number()]).describe('Search center [longitude, latitude]')
    }) as any,
    func: async ({ category, location }: any) => {
      return await mcp.callTool('category_search_tool', {
        category,
        proximity: { longitude: location[0], latitude: location[1] }
      });
    }
  }),

  new DynamicStructuredTool({
    name: 'isochrone_tool',
    description:
      'Calculate the AREA reachable within a time limit from a starting point. Use for "What can I reach in X minutes?" questions.',
    schema: z.object({
      location: z.tuple([z.number(), z.number()]).describe('Center point [longitude, latitude]'),
      minutes: z.number().describe('Time limit in minutes'),
      profile: z.enum(['mapbox/driving', 'mapbox/walking', 'mapbox/cycling']).optional()
    }) as any,
    func: async ({ location, minutes, profile }: any) => {
      return await mcp.callTool('isochrone_tool', {
        coordinates: { longitude: location[0], latitude: location[1] },
        contours_minutes: [minutes],
        profile: profile || 'mapbox/walking'
      });
    }
  }),

  new DynamicStructuredTool({
    name: 'distance_tool',
    description: 'Calculate straight-line distance between two points (offline, free)',
    schema: z.object({
      from: z.tuple([z.number(), z.number()]).describe('Start [longitude, latitude]'),
      to: z.tuple([z.number(), z.number()]).describe('End [longitude, latitude]'),
      units: z.enum(['miles', 'kilometers']).optional()
    }) as any,
    func: async ({ from, to, units }: any) => {
      return await mcp.callTool('distance_tool', {
        from: { longitude: from[0], latitude: from[1] },
        to: { longitude: to[0], latitude: to[1] },
        units: units || 'miles'
      });
    }
  })
];

// Create agent
const llm = new ChatOpenAI({ model: 'gpt-5.2', temperature: 0 });
const prompt = ChatPromptTemplate.fromMessages([
  ['system', 'You are a location intelligence assistant.'],
  ['human', '{input}'],
  new MessagesPlaceholder('agent_scratchpad')
]);
// @ts-ignore - Zod tuple schemas cause deep type recursion
const agent = await createToolCallingAgent({ llm, tools, prompt });
const executor = new AgentExecutor({ agent, tools, verbose: true });

// Use agent
const result = await executor.invoke({
  input: 'Find coffee shops within 10 minutes walking from Union Square, NYC'
});
```

**Benefits:**

- Conversational interface
- Tool chaining
- Memory and context management

**TypeScript Type Considerations:**

When using `DynamicStructuredTool` with Zod schemas (especially `z.tuple()`), TypeScript may encounter deep type recursion errors. This is a known limitation with complex Zod generic types. The minimal fix is to add `as any` type assertions:

```typescript
const tool = new DynamicStructuredTool({
  name: 'my_tool',
  schema: z.object({
    coords: z.tuple([z.number(), z.number()])
  }) as any, // ← Add 'as any' to prevent type recursion
  func: async ({ coords }: any) => {
    // ← Type parameters as 'any'
    // Implementation
  }
});

// For JSON responses from external APIs
const data = (await response.json()) as any;

// For createOpenAIFunctionsAgent with complex tool types
// @ts-ignore - Zod tuple schemas cause deep type recursion
const agent = await createOpenAIFunctionsAgent({ llm, tools, prompt });
```

This doesn't affect runtime validation (Zod still validates at runtime) - it only helps TypeScript's type checker avoid infinite recursion during compilation.

### Pattern 6: Custom Agent Integration

**Use case:** Building domain-specific AI applications (Zillow-style, TripAdvisor-style)

```typescript
interface MCPTool {
  name: string;
  description: string;
  inputSchema: any;
}

class CustomMapboxAgent {
  private url = 'https://mcp.mapbox.com/mcp';
  private headers: Record<string, string>;
  private tools: Map<string, MCPTool> = new Map();

  constructor(token?: string) {
    const mapboxToken = token || process.env.MAPBOX_ACCESS_TOKEN;
    this.headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${mapboxToken}`
    };
  }

  async initialize() {
    // Discover available tools from MCP server
    await this.discoverTools();
  }

  private async discoverTools() {
    const request = {
      jsonrpc: '2.0',
      id: 1,
      method: 'tools/list'
    };

    const response = await this.sendMCPRequest(request);
    response.result.tools.forEach((tool: MCPTool) => {
      this.tools.set(tool.name, tool);
    });
  }

  async callTool(toolName: string, params: any): Promise<any> {
    const request = {
      jsonrpc: '2.0',
      id: Date.now(),
      method: 'tools/call',
      params: { name: toolName, arguments: params }
    };

    const response = await this.sendMCPRequest(request);
    return response.result.content[0].text;
  }

  private async sendMCPRequest(request: any): Promise<any> {
    const response = await fetch(this.url, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(request)
    });

    const data = await response.json();

    if (data.error) {
      throw new Error(data.error.message);
    }

    return data;
  }

  // Domain-specific methods
  async findPropertiesWithCommute(
    homeLocation: [number, number],
    workLocation: [number, number],
    maxCommuteMinutes: number
  ) {
    // Get isochrone from work location
    const isochrone = await this.callTool('isochrone_tool', {
      coordinates: { longitude: workLocation[0], latitude: workLocation[1] },
      contours_minutes: [maxCommuteMinutes],
      profile: 'mapbox/driving-traffic'
    });

    // Check if home is within isochrone
    const isInRange = await this.callTool('point_in_polygon_tool', {
      point: { longitude: homeLocation[0], latitude: homeLocation[1] },
      polygon: JSON.parse(isochrone).features[0].geometry
    });

    return JSON.parse(isInRange);
  }

  async findRestaurantsNearby(location: [number, number], radiusMiles: number) {
    // Search restaurants
    const results = await this.callTool('category_search_tool', {
      category: 'restaurant',
      proximity: { longitude: location[0], latitude: location[1] }
    });

    // Filter by distance
    const restaurants = JSON.parse(results);
    const filtered = [];

    for (const restaurant of restaurants) {
      const distance = await this.callTool('distance_tool', {
        from: { longitude: location[0], latitude: location[1] },
        to: { longitude: restaurant.coordinates[0], latitude: restaurant.coordinates[1] },
        units: 'miles'
      });

      if (parseFloat(distance) <= radiusMiles) {
        filtered.push({
          ...restaurant,
          distance: parseFloat(distance)
        });
      }
    }

    return filtered.sort((a, b) => a.distance - b.distance);
  }
}

// Usage in Zillow-style app
const agent = new CustomMapboxAgent();
await agent.initialize();

const properties = await agent.findPropertiesWithCommute(
  [-122.4194, 37.7749], // Home in SF
  [-122.4, 37.79], // Work downtown
  30 // Max 30min commute
);

// Usage in TripAdvisor-style app
const restaurants = await agent.findRestaurantsNearby(
  [-73.9857, 40.7484], // Times Square
  0.5 // Within 0.5 miles
);
```

**Benefits:**

- Full control over agent behavior
- Domain-specific abstractions
- Custom error handling

## Architecture Patterns

### Pattern: MCP as Service Layer

```
┌─────────────────────────────────────┐
│         Your Application            │
│  (Next.js, Express, FastAPI, etc.)  │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│        AI Agent Layer               │
│   (pydantic-ai, mastra, custom)     │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│     Mapbox MCP Server               │
│  (Geospatial tools abstraction)     │
└────────────────┬────────────────────┘
                 │
          ┌──────┴──────┐
          ▼             ▼
    ┌─────────┐   ┌──────────┐
    │ Turf.js │   │ Mapbox   │
    │ (Local) │   │   APIs   │
    └─────────┘   └──────────┘
```

**Benefits:**

- Clean separation of concerns
- Easy to swap MCP server versions
- Centralized geospatial logic

### Pattern: Hybrid Approach

You can use MCP for AI agent features while using direct Mapbox APIs for other parts of your app.

```typescript
class GeospatialService {
  constructor(
    private mcpServer: MapboxMCPServer, // For AI features
    private mapboxSdk: MapboxSDK // For direct app features
  ) {}

  // AI Agent Feature: Natural language search
  async aiSearchNearby(userQuery: string): Promise<string> {
    // Let AI agent use MCP tools to interpret query and find places
    // Returns natural language response
    return await this.agent.execute(userQuery, [
      this.mcpServer.tools.category_search_tool,
      this.mcpServer.tools.directions_tool
    ]);
  }

  // Direct App Feature: Display route on map
  async getRouteGeometry(origin: Point, dest: Point): Promise<LineString> {
    // Direct API call for map rendering - returns GeoJSON
    const result = await this.mapboxSdk.directions.getDirections({
      waypoints: [origin, dest],
      geometries: 'geojson'
    });
    return result.routes[0].geometry;
  }

  // Offline Feature: Distance calculations (always use MCP/Turf.js)
  async calculateDistance(from: Point, to: Point): Promise<number> {
    // No API cost, instant
    return await this.mcpServer.callTool('distance_tool', {
      from,
      to,
      units: 'miles'
    });
  }
}
```

**Architecture Decision Guide:**

| Use Case                           | Use This                   | Why                                              |
| ---------------------------------- | -------------------------- | ------------------------------------------------ |
| AI agent natural language features | MCP Server                 | Simplified tool interface, AI-friendly responses |
| Map rendering, direct UI controls  | Mapbox SDK                 | More control, better performance                 |
| Distance/area calculations         | MCP Server (offline tools) | Free, instant, no API calls                      |
| Custom map styling                 | Mapbox SDK                 | Fine-grained style control                       |
| Conversational geospatial queries  | MCP Server                 | AI agent can chain tools                         |

## Use Cases by Application Type

### Real Estate App (Zillow-style)

```typescript
// Find properties with good commute
async findPropertiesByCommute(
  searchArea: Polygon,
  workLocation: Point,
  maxCommuteMinutes: number
) {
  // 1. Get isochrone from work
  const reachableArea = await mcp.callTool('isochrone_tool', {
    coordinates: { longitude: workLocation[0], latitude: workLocation[1] },
    contours_minutes: [maxCommuteMinutes],
    profile: 'mapbox/driving'
  });

  // 2. Check each property
  const propertiesInRange = [];
  for (const property of properties) {
    const inRange = await mcp.callTool('point_in_polygon_tool', {
      point: { longitude: property.location[0], latitude: property.location[1] },
      polygon: reachableArea
    });

    if (inRange) {
      // 3. Get exact commute time
      const directions = await mcp.callTool('directions_tool', {
        coordinates: [property.location, workLocation],
        routing_profile: 'mapbox/driving-traffic'
      });

      propertiesInRange.push({
        ...property,
        commuteTime: directions.duration / 60
      });
    }
  }

  return propertiesInRange;
}
```

### Food Delivery App (DoorDash-style)

```typescript
// Check if restaurant can deliver to address
async canDeliver(
  restaurantLocation: Point,
  deliveryAddress: Point,
  maxDeliveryTime: number
) {
  // 1. Calculate delivery zone
  const deliveryZone = await mcp.callTool('isochrone_tool', {
    coordinates: restaurantLocation,
    contours_minutes: [maxDeliveryTime],
    profile: 'mapbox/driving'
  });

  // 2. Check if address is in zone
  const canDeliver = await mcp.callTool('point_in_polygon_tool', {
    point: deliveryAddress,
    polygon: deliveryZone
  });

  if (!canDeliver) return false;

  // 3. Get accurate delivery time
  const route = await mcp.callTool('directions_tool', {
    coordinates: [restaurantLocation, deliveryAddress],
    routing_profile: 'mapbox/driving-traffic'
  });

  return {
    canDeliver: true,
    estimatedTime: route.duration / 60,
    distance: route.distance
  };
}
```

### Travel Planning App (TripAdvisor-style)

```typescript
// Build day itinerary with travel times
async buildItinerary(
  hotel: Point,
  attractions: Array<{name: string, location: Point}>
) {
  // 1. Calculate distances from hotel
  const attractionsWithDistance = await Promise.all(
    attractions.map(async (attr) => ({
      ...attr,
      distance: await mcp.callTool('distance_tool', {
        from: hotel,
        to: attr.location,
        units: 'miles'
      })
    }))
  );

  // 2. Get travel time matrix
  const matrix = await mcp.callTool('matrix_tool', {
    origins: [hotel],
    destinations: attractions.map(a => a.location),
    profile: 'mapbox/walking'
  });

  // 3. Sort by walking time
  return attractionsWithDistance
    .map((attr, idx) => ({
      ...attr,
      walkingTime: matrix.durations[0][idx] / 60
    }))
    .sort((a, b) => a.walkingTime - b.walkingTime);
}
```

## Performance Optimization

### Caching Strategy

```typescript
class CachedMapboxMCP {
  private cache = new Map<string, { result: any; timestamp: number }>();
  private cacheTTL = 3600000; // 1 hour

  async callTool(name: string, params: any): Promise<any> {
    // Cache offline tools indefinitely (deterministic)
    const offlineTools = ['distance_tool', 'point_in_polygon_tool', 'bearing_tool'];
    const ttl = offlineTools.includes(name) ? Infinity : this.cacheTTL;

    // Check cache
    const cacheKey = JSON.stringify({ name, params });
    const cached = this.cache.get(cacheKey);

    if (cached && Date.now() - cached.timestamp < ttl) {
      return cached.result;
    }

    // Call MCP
    const result = await this.mcpServer.callTool(name, params);

    // Store in cache
    this.cache.set(cacheKey, {
      result,
      timestamp: Date.now()
    });

    return result;
  }
}
```

### Batch Operations

```typescript
// ❌ Bad: Sequential calls
for (const location of locations) {
  const distance = await mcp.callTool('distance_tool', {
    from: userLocation,
    to: location
  });
}

// ✅ Good: Parallel batch
const distances = await Promise.all(
  locations.map((location) =>
    mcp.callTool('distance_tool', {
      from: userLocation,
      to: location
    })
  )
);

// ✅ Better: Use matrix tool
const matrix = await mcp.callTool('matrix_tool', {
  origins: [userLocation],
  destinations: locations
});
```

### Writing Effective Tool Descriptions

Clear, specific tool descriptions are critical for helping LLMs select the right tools. Poor descriptions lead to incorrect tool calls, wasted API requests, and user frustration.

#### Common Confusion Points

**Problem: "How far is it from A to B?"** - Could trigger either `directions_tool` OR `distance_tool`

```typescript
// ❌ Ambiguous descriptions
{
  name: 'directions_tool',
  description: 'Get directions between two locations'  // Could mean distance
}
{
  name: 'distance_tool',
  description: 'Calculate distance between two points'  // Unclear what kind
}

// ✅ Clear, specific descriptions
{
  name: 'directions_tool',
  description: 'Get turn-by-turn driving directions with traffic-aware route distance and travel time. Use when you need the actual route, navigation instructions, or driving duration. Returns route geometry, distance along roads, and time estimate.'
}
{
  name: 'distance_tool',
  description: 'Calculate straight-line (great-circle) distance between two points. Use for quick "as the crow flies" distance checks, proximity comparisons, or when routing is not needed. Works offline, instant, no API cost.'
}
```

**Problem: "Find coffee shops nearby"** - Could trigger `category_search_tool` OR `search_and_geocode_tool`

```typescript
// ❌ Ambiguous
{
  name: 'search_poi',
  description: 'Search for places'
}

// ✅ Clear when to use each
{
  name: 'category_search_tool',
  description: 'Find ALL places of a specific type/category (e.g., "all coffee shops", "restaurants", "gas stations") near a location. Use for browsing or discovering places by category. Returns multiple results.'
}
{
  name: 'search_and_geocode_tool',
  description: 'Search for a SPECIFIC named place or address (e.g., "Starbucks on Main St", "123 Market St"). Use when the user provides a business name, street address, or landmark. Returns best match.'
}
```

**Problem: "Where can I go in 15 minutes?"** - Could trigger `isochrone_tool` OR `directions_tool`

```typescript
// ❌ Confusing
{
  name: 'isochrone_tool',
  description: 'Calculate travel time area'
}

// ✅ Clear distinction
{
  name: 'isochrone_tool',
  description: 'Calculate the AREA reachable within a time limit from a starting point. Returns a GeoJSON polygon showing everywhere you can reach. Use for: "What can I reach in X minutes?", service area analysis, catchment zones, delivery zones.'
}
{
  name: 'directions_tool',
  description: 'Get route from point A to specific point B. Returns turn-by-turn directions to ONE destination. Use for: "How do I get to X?", "Route from A to B", navigation to a known destination.'
}
```

#### Best Practices for Tool Descriptions

1. **Start with the primary use case** in simple terms
2. **Explain WHEN to use this tool** vs alternatives
3. **Include key distinguishing details**: Does it use traffic? Is it offline? Does it cost API calls?
4. **Give concrete examples** of questions that should trigger this tool
5. **Mention what it returns** so LLMs know if it fits the user's need

```typescript
// ✅ Complete example
const searchPOITool = new DynamicStructuredTool({
  name: 'category_search_tool',
  description: `Find places by category type (restaurants, hotels, coffee shops, gas stations, etc.) near a location.

  Use when the user wants to:
  - Browse places of a certain type: "coffee shops nearby", "find restaurants"
  - Discover options: "what hotels are in this area?"
  - Search by industry/amenity, not by specific name

  Returns: List of matching places with names, addresses, and coordinates.

  DO NOT use for:
  - Specific named places (use search_and_geocode_tool instead)
  - Addresses (use search_and_geocode_tool or reverse_geocode_tool)`
  // ... schema and implementation
});
```

#### System Prompt Guidance

Add tool selection guidance to your agent's system prompt:

```typescript
const systemPrompt = `You are a location intelligence assistant.

TOOL SELECTION RULES:
- Use distance_tool for straight-line distance ("as the crow flies")
- Use directions_tool for route distance along roads with traffic
- Use category_search_tool for finding types of places ("coffee shops")
- Use search_and_geocode_tool for specific addresses or named places ("123 Main St", "Starbucks downtown")
- Use isochrone_tool for "what can I reach in X minutes" questions
- Use offline tools (distance_tool, point_in_polygon_tool) when real-time data is not needed

When in doubt, prefer:
1. Offline tools over API calls (faster, free)
2. Specific tools over general ones
3. Asking for clarification over guessing`;
```

### Tool Selection

```typescript
// Use offline tools when possible (faster, free)
const localOps = {
  distance: 'distance_tool', // Turf.js
  pointInPolygon: 'point_in_polygon_tool', // Turf.js
  bearing: 'bearing_tool', // Turf.js
  area: 'area_tool' // Turf.js
};

// Use API tools when necessary (requires token, slower)
const apiOps = {
  directions: 'directions_tool', // Mapbox API
  geocoding: 'reverse_geocode_tool', // Mapbox API
  isochrone: 'isochrone_tool', // Mapbox API
  search: 'category_search_tool' // Mapbox API
};

// Choose based on requirements
function chooseTool(operation: string, needsRealtime: boolean) {
  if (needsRealtime) {
    return apiOps[operation]; // Traffic, live data
  }
  return localOps[operation] || apiOps[operation];
}
```

## Error Handling

```typescript
class RobustMapboxMCP {
  async callToolWithRetry(name: string, params: any, maxRetries: number = 3): Promise<any> {
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await this.mcpServer.callTool(name, params);
      } catch (error) {
        if (error.code === 'RATE_LIMIT') {
          // Exponential backoff
          await this.sleep(Math.pow(2, i) * 1000);
          continue;
        }

        if (error.code === 'INVALID_TOKEN') {
          // Non-retryable error
          throw error;
        }

        if (i === maxRetries - 1) {
          throw error;
        }
      }
    }
  }

  async callToolWithFallback(primaryTool: string, fallbackTool: string, params: any): Promise<any> {
    try {
      return await this.callTool(primaryTool, params);
    } catch (error) {
      console.warn(`Primary tool ${primaryTool} failed, using fallback`);
      return await this.callTool(fallbackTool, params);
    }
  }
}
```

## Security Best Practices

### Token Management

```typescript
// ✅ Good: Use environment variables
const mcp = new MapboxMCP({
  token: process.env.MAPBOX_ACCESS_TOKEN
});

// ❌ Bad: Hardcode tokens
const mcp = new MapboxMCP({
  token: 'pk.ey...' // Never do this!
});

// ✅ Good: Use scoped tokens
// Create token with minimal scopes:
// - directions:read
// - geocoding:read
// - No write permissions
```

### Rate Limiting

```typescript
class RateLimitedMCP {
  private requestQueue: Array<() => Promise<any>> = [];
  private requestsPerMinute = 300;
  private currentMinute = Math.floor(Date.now() / 60000);
  private requestCount = 0;

  async callTool(name: string, params: any): Promise<any> {
    // Check rate limit
    const minute = Math.floor(Date.now() / 60000);
    if (minute !== this.currentMinute) {
      this.currentMinute = minute;
      this.requestCount = 0;
    }

    if (this.requestCount >= this.requestsPerMinute) {
      // Wait until next minute
      const waitMs = (this.currentMinute + 1) * 60000 - Date.now();
      await this.sleep(waitMs);
    }

    this.requestCount++;
    return await this.mcpServer.callTool(name, params);
  }
}
```

## Testing

```typescript
// Mock MCP server for testing
class MockMapboxMCP {
  async callTool(name: string, params: any): Promise<any> {
    const mocks = {
      distance_tool: () => '2.5',
      directions_tool: () => JSON.stringify({
        duration: 1200,
        distance: 5000,
        geometry: {...}
      }),
      point_in_polygon_tool: () => 'true'
    };

    return mocks[name]?.() || '{}';
  }
}

// Use in tests
describe('Property search', () => {
  it('finds properties within commute time', async () => {
    const agent = new CustomMapboxAgent(new MockMapboxMCP());
    const results = await agent.findPropertiesWithCommute(
      [-122.4, 37.7],
      [-122.41, 37.78],
      30
    );

    expect(results).toHaveLength(5);
  });
});
```

## Resources

- [Mapbox MCP Server](https://github.com/mapbox/mcp-server)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Pydantic AI](https://ai.pydantic.dev/)
- [Mastra](https://mastra.ai/)
- [LangChain](https://docs.langchain.com/oss/javascript/langchain/overview/)
- [Mapbox API Documentation](https://docs.mapbox.com/api/)

## When to Use This Skill

Invoke this skill when:

- Integrating Mapbox MCP Server into AI applications
- Building AI agents with geospatial capabilities
- Architecting Zillow/TripAdvisor/DoorDash-style apps with AI
- Choosing between MCP, direct APIs, or SDKs
- Optimizing geospatial operations in production
- Implementing error handling for geospatial AI features
- Testing AI applications with geospatial tools
