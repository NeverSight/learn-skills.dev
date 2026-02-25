---
name: hytale-ui
description: Custom user interface and HUD creation for Hytale. Covers NoesisGUI framework, custom HUD overlays, menus, inventory screens, and interactive UI elements. Use when creating custom interfaces, status displays, admin panels, or any visual UI components.
---

# Hytale UI & HUD

Create custom user interfaces and HUD elements for your Hytale mods.

## UI Framework

Hytale uses **NoesisGUI** - a powerful XAML-based UI framework.

## UI Types

| Type | Use For | Examples |
|------|---------|----------|
| **HUD** | Always-on-screen | Health, mana, minimap |
| **Overlay** | Temporary display | Notifications, titles |
| **Screen** | Full interface | Inventory, menus |
| **Dialog** | Popups | Confirmations, NPC chat |
| **Widget** | Reusable components | Buttons, bars, icons |

---

## Folder Structure

```
MyPack/
└── Common/
    └── UI/
        ├── hud/
        │   ├── my_hud.xaml
        │   └── my_hud.xaml.cs
        ├── screens/
        │   ├── custom_menu.xaml
        │   └── custom_inventory.xaml
        └── textures/
            ├── button_bg.png
            └── icons/
```

---

## Basic HUD Element

### XAML Definition

```xml
<!-- my_hud.xaml -->
<UserControl 
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    
    <Grid HorizontalAlignment="Left" VerticalAlignment="Top" Margin="10">
        <!-- Mana Bar -->
        <Border Background="#333" CornerRadius="5" Padding="2">
            <Grid Width="200" Height="20">
                <Rectangle Fill="#224" RadiusX="3" RadiusY="3"/>
                <Rectangle x:Name="ManaFill" Fill="#48F" RadiusX="3" RadiusY="3"
                           HorizontalAlignment="Left" Width="150"/>
                <TextBlock Text="150/200" Foreground="White" 
                           HorizontalAlignment="Center" VerticalAlignment="Center"/>
            </Grid>
        </Border>
    </Grid>
</UserControl>
```

### JSON Registration

```json
{
  "hudId": "mymod:mana_bar",
  "xaml": "ui/hud/mana_bar.xaml",
  "position": "top-left",
  "offset": { "x": 10, "y": 50 }
}
```

---

## HUD Positions

| Position | Description |
|----------|-------------|
| `top-left` | Upper left corner |
| `top-center` | Upper center |
| `top-right` | Upper right corner |
| `center` | Screen center |
| `bottom-left` | Lower left |
| `bottom-center` | Lower center |
| `bottom-right` | Lower right |

---

## Common UI Components

### Progress Bar

```xml
<Grid Width="200" Height="20">
    <Rectangle Fill="#333" RadiusX="3" RadiusY="3"/>
    <Rectangle x:Name="ProgressFill" Fill="#4A4" RadiusX="3" RadiusY="3"
               HorizontalAlignment="Left" Width="{Binding Progress}"/>
    <TextBlock Text="{Binding ProgressText}" Foreground="White"
               HorizontalAlignment="Center" VerticalAlignment="Center"/>
</Grid>
```

### Icon Button

```xml
<Button Width="48" Height="48" Style="{StaticResource IconButton}">
    <Image Source="textures/icons/sword.png" Width="32" Height="32"/>
</Button>
```

### Tooltip

```xml
<Border Background="#222" CornerRadius="5" Padding="10">
    <StackPanel>
        <TextBlock Text="{Binding ItemName}" FontWeight="Bold" Foreground="#FF0"/>
        <TextBlock Text="{Binding ItemDesc}" Foreground="#AAA" TextWrapping="Wrap"/>
    </StackPanel>
</Border>
```

---

## Custom Screens

### Menu Screen

```xml
<UserControl>
    <Grid Background="#88000000">
        <Border Background="#333" CornerRadius="10" Padding="20"
                HorizontalAlignment="Center" VerticalAlignment="Center">
            <StackPanel Width="300">
                <TextBlock Text="My Custom Menu" FontSize="24" 
                           Foreground="White" HorizontalAlignment="Center"/>
                
                <Button Content="Option 1" Margin="0,20,0,0" Height="40"/>
                <Button Content="Option 2" Margin="0,10,0,0" Height="40"/>
                <Button Content="Close" Margin="0,20,0,0" Height="40"
                        Click="OnClose"/>
            </StackPanel>
        </Border>
    </Grid>
</UserControl>
```

### Inventory Grid

```xml
<ItemsControl ItemsSource="{Binding InventorySlots}">
    <ItemsControl.ItemsPanel>
        <ItemsPanelTemplate>
            <UniformGrid Columns="9" Rows="4"/>
        </ItemsPanelTemplate>
    </ItemsControl.ItemsPanel>
    <ItemsControl.ItemTemplate>
        <DataTemplate>
            <Border Width="48" Height="48" Background="#444" 
                    BorderBrush="#666" BorderThickness="1" Margin="2">
                <Image Source="{Binding Icon}" Stretch="Uniform"/>
            </Border>
        </DataTemplate>
    </ItemsControl.ItemTemplate>
</ItemsControl>
```

---

## Plugin Integration

### Show/Hide HUD

```java
// Show custom HUD
player.showHUD("mymod:mana_bar");

// Hide HUD
player.hideHUD("mymod:mana_bar");

// Check if visible
boolean visible = player.isHUDVisible("mymod:mana_bar");
```

### Update HUD Data

```java
// Update bound data
player.setHUDData("mymod:mana_bar", "mana", currentMana);
player.setHUDData("mymod:mana_bar", "maxMana", maxMana);

// Or with object
ManaData data = new ManaData(currentMana, maxMana);
player.setHUDData("mymod:mana_bar", data);
```

### Open Screens

```java
// Open custom screen
player.openScreen("mymod:custom_menu");

// Open with data
player.openScreen("mymod:shop", shopInventory);

// Close current screen
player.closeScreen();
```

### Notifications

```java
// Show toast notification
player.showNotification("Achievement Unlocked!", 5.0f);

// Show title
player.showTitle("Boss Defeated!", "You earned 500 XP", 3.0f);

// Show action bar message
player.showActionBar("Press E to interact");
```

---

## Data Binding

### ViewModel Pattern

```java
public class ManaViewModel {
    private int mana;
    private int maxMana;
    
    public int getMana() { return mana; }
    public void setMana(int value) {
        this.mana = value;
        notifyPropertyChanged("mana");
        notifyPropertyChanged("manaPercent");
    }
    
    public double getManaPercent() {
        return (double) mana / maxMana * 100;
    }
}
```

### In XAML

```xml
<Rectangle Width="{Binding ManaPercent, Converter={StaticResource PercentToWidth}}"/>
<TextBlock Text="{Binding Mana, StringFormat='{}{0} MP'}"/>
```

---

## Styling

### Custom Button Style

```xml
<Style x:Key="GameButton" TargetType="Button">
    <Setter Property="Background" Value="#444"/>
    <Setter Property="Foreground" Value="White"/>
    <Setter Property="BorderBrush" Value="#666"/>
    <Setter Property="BorderThickness" Value="2"/>
    <Setter Property="Padding" Value="15,8"/>
    <Setter Property="FontSize" Value="14"/>
    <Style.Triggers>
        <Trigger Property="IsMouseOver" Value="True">
            <Setter Property="Background" Value="#555"/>
            <Setter Property="BorderBrush" Value="#888"/>
        </Trigger>
        <Trigger Property="IsPressed" Value="True">
            <Setter Property="Background" Value="#333"/>
        </Trigger>
    </Style.Triggers>
</Style>
```

### Color Palette

```xml
<Color x:Key="PrimaryColor">#4A90D9</Color>
<Color x:Key="SecondaryColor">#2ECC71</Color>
<Color x:Key="DangerColor">#E74C3C</Color>
<Color x:Key="BackgroundColor">#2C3E50</Color>
<Color x:Key="TextColor">#ECF0F1</Color>
```

---

## Best Practices

### Do

| Practice | Why |
|----------|-----|
| Use data binding | Automatic updates |
| Consistent styling | Professional look |
| Test all resolutions | Accessibility |
| Provide feedback | User understands |

### Don't

| Mistake | Why Bad |
|---------|---------|
| Too many HUDs | Screen clutter |
| Tiny text | Hard to read |
| No close button | Frustrating |
| Block gameplay | Annoying |

---

## Quick Reference

| Task | How |
|------|-----|
| Create HUD | Define XAML + register JSON |
| Show HUD | `player.showHUD("id")` |
| Update data | `player.setHUDData(...)` |
| Open screen | `player.openScreen("id")` |
| Show notification | `player.showNotification(...)` |

---

## Resources

- **NoesisGUI Docs**: [noesisengine.com](https://www.noesisengine.com/docs)
- **Plugin Development**: See `hytale-plugin-dev` skill
- **NPC Dialogue**: See `hytale-npc-ai` skill
