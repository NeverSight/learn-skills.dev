---
name: playwright-llm
description: Browser automation using Playwright for web navigation, content extraction, and interaction. Use when you need to browse websites, scrape content, or interact with web pages.
---

# PlaywrightLLM Browser Automation

This skill provides tools for automating web browser interactions using Playwright. It maintains a persistent Chromium browser session and offers tools for navigation, content extraction, clicking elements, form submission, and web search.

## Installation

PlaywrightLLM is implemented as a Ruby gem. Add it to your Gemfile:

```ruby
gem 'playwright_llm', :github => 'plerohellec/playwright_llm'
```

Then run `bundle install` to install the gem and its dependencies.

## Available Tools

### Navigate
Navigates to a URL and returns the HTTP status code.
- **Parameters**: `url` (string, required) - The URL to navigate to

### SlimHtml
Extracts cleaned HTML content from the current page, removing scripts and styles. Returns content in chunks.
- **Parameters**: `chunk` (integer, optional, default 1) - Chunk number to retrieve

### Click
Clicks on a CSS selector and waits for the page to settle.
- **Parameters**: `selector` (string, required) - CSS selector to click

### FullHtml
Extracts full HTML content within a specific ID selector.
- **Parameters**: `selector` (string, required) - ID selector like #myId

### SearchForm
Fills and submits a search form.
- **Parameters**: `form_id` (string, required), `search_term` (string, required)

### ParallelSearch
Searches the web using Parallel.ai API (requires API key).
- **Parameters**: `query` (string, required)

### Executor
Executes custom Playwright JavaScript code.
- **Parameters**: `script_code` (string, required)

## Usage

To use PlaywrightLLM, write a Ruby script that:

1. Requires the necessary libraries
2. Launches a browser session
3. Uses the tools to interact with web pages
4. Closes the browser when done

### Script Setup

```ruby
require 'playwright_llm'

logger = PlaywrightLLM.logger

# Launch browser
browser = PlaywrightLLM::Browser.new(logger: logger)
res = browser.execute()
unless res[:success]
  puts "Failed to launch browser: #{res[:error]}"
  exit 1
end
```

### Using Tools

Each tool is a Ruby class that you instantiate and call `execute` on with parameters:

```ruby
# Navigate to a URL
nav_tool = PlaywrightLLM::Tools::Navigate.new
result = nav_tool.execute(url: "https://example.com")

# Click on an element
click_tool = PlaywrightLLM::Tools::Click.new
result = click_tool.execute(selector: "#button-id")

# Extract cleaned HTML
slim_tool = PlaywrightLLM::Tools::SlimHtml.new
html = slim_tool.execute()  # or execute(chunk: 2) for next chunk
```

### Example Script

Here's a complete example that navigates to a URL, clicks a selector, and extracts the HTML:

```ruby
#!/usr/bin/env ruby

require 'bundler/setup'
Bundler.require(:default)

require 'playwright_llm'

logger = PlaywrightLLM.logger

# Launch browser
browser = PlaywrightLLM::Browser.new(logger: logger)
res = browser.execute()

unless res[:success]
  puts "Failed to launch browser: #{res[:error]}"
  exit 1
end

# Navigate to URL
nav_tool = PlaywrightLLM::Tools::Navigate.new
nav_result = nav_tool.execute(url: "https://example.com")

if nav_result.is_a?(Hash) && nav_result[:error]
  puts "Navigation failed: #{nav_result[:error]}"
  browser.close
  exit 1
end

# Click on a selector
click_tool = PlaywrightLLM::Tools::Click.new
click_result = click_tool.execute(selector: "#some-button")

if click_result.is_a?(Hash) && click_result[:error]
  puts "Click failed: #{click_result[:error]}"
  browser.close
  exit 1
end

# Extract HTML
slim_tool = PlaywrightLLM::Tools::SlimHtml.new
html = slim_tool.execute()

if html.is_a?(Hash) && html[:error]
  puts "HTML extraction failed: #{html[:error]}"
  browser.close
  exit 1
end

puts html

browser.close
```

### Error Handling

Tools return either the result data or a hash with an `:error` key. Always check for errors:

```ruby
result = some_tool.execute(params)
if result.is_a?(Hash) && result[:error]
  puts "Tool failed: #{result[:error]}"
  # handle error
end
```

## Requirements

- Node.js with Playwright
- Chromium browser
- API keys for LLM providers and optional web search