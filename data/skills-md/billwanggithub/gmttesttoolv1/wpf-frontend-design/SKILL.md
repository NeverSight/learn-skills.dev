---
name: wpf-frontend-design
description: WPF 桌面應用程式的專業 UI/UX 設計指南，打造現代化、高品質的視覺體驗
---

# WPF Frontend Design

這個命令專門針對 WPF 桌面應用程式的 UI/UX 設計，提供從樣式系統到自訂控制項的完整指南。

## 🎯 核心目標

**創造專業、現代化的 WPF 應用程式**，超越預設的 Windows 外觀，打造具有品牌識別度和卓越使用者體驗的桌面應用。

## 設計哲學

### 1. WPF 不是 Web

❌ **避免**：

- 試圖模仿網頁設計
- 過度使用圓角和陰影
- 忽視桌面應用的特性（視窗管理、鍵盤導航等）

✅ **擁抱**：

- 桌面應用的優勢（豐富的控制項、本地效能）
- Windows 設計語言的精髓
- 原生的視覺層次和深度

### 2. 效能優先

WPF 的渲染特性：

- 向量圖形（不失真）
- 硬體加速
- 但要避免過度繪製和複雜的視覺樹

### 3. 可存取性

桌面應用必須支援：

- 鍵盤完整操作
- 螢幕閱讀器
- 高對比度模式
- 縮放和 DPI 感知

---

## 🎨 設計系統架構

### 資源字典結構

建議的資源字典組織：

```
Resources/
├── Colors.xaml          # 色彩定義
├── Fonts.xaml           # 字體樣式
├── Brushes.xaml         # 筆刷（漸層、圖案）
├── Styles/
│   ├── ButtonStyles.xaml
│   ├── TextBoxStyles.xaml
│   ├── ListBoxStyles.xaml
│   └── ...
├── Templates/
│   ├── WindowTemplate.xaml
│   ├── DataGridTemplate.xaml
│   └── ...
└── Themes/
    ├── LightTheme.xaml
    └── DarkTheme.xaml
```

### 色彩系統

```xml
<!-- Resources/Colors.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <!-- 基礎色彩 - 使用 WPF Color 而非 Hex -->
    <Color x:Key="PrimaryColor">#2196F3</Color>
    <Color x:Key="PrimaryLightColor">#64B5F6</Color>
    <Color x:Key="PrimaryDarkColor">#1976D2</Color>

    <Color x:Key="AccentColor">#FF9800</Color>
    <Color x:Key="AccentLightColor">#FFB74D</Color>
    <Color x:Key="AccentDarkColor">#F57C00</Color>

    <!-- 語義色彩 -->
    <Color x:Key="SuccessColor">#4CAF50</Color>
    <Color x:Key="WarningColor">#FFC107</Color>
    <Color x:Key="ErrorColor">#F44336</Color>
    <Color x:Key="InfoColor">#2196F3</Color>

    <!-- 中性色 -->
    <Color x:Key="BackgroundColor">#FFFFFF</Color>
    <Color x:Key="SurfaceColor">#F5F5F5</Color>
    <Color x:Key="BorderColor">#E0E0E0</Color>

    <Color x:Key="TextPrimaryColor">#212121</Color>
    <Color x:Key="TextSecondaryColor">#757575</Color>
    <Color x:Key="TextDisabledColor">#BDBDBD</Color>

    <!-- Dark Theme -->
    <Color x:Key="DarkBackgroundColor">#121212</Color>
    <Color x:Key="DarkSurfaceColor">#1E1E1E</Color>
    <Color x:Key="DarkBorderColor">#2C2C2C</Color>

    <Color x:Key="DarkTextPrimaryColor">#FFFFFF</Color>
    <Color x:Key="DarkTextSecondaryColor">#B0B0B0</Color>
</ResourceDictionary>
```

### 筆刷系統

```xml
<!-- Resources/Brushes.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <!-- 合併色彩資源 -->
    <ResourceDictionary.MergedDictionaries>
        <ResourceDictionary Source="Colors.xaml"/>
    </ResourceDictionary.MergedDictionaries>

    <!-- 實心筆刷 -->
    <SolidColorBrush x:Key="PrimaryBrush" Color="{StaticResource PrimaryColor}"/>
    <SolidColorBrush x:Key="PrimaryLightBrush" Color="{StaticResource PrimaryLightColor}"/>
    <SolidColorBrush x:Key="AccentBrush" Color="{StaticResource AccentColor}"/>

    <!-- 半透明筆刷 -->
    <SolidColorBrush x:Key="OverlayBrush" Color="{StaticResource PrimaryColor}" Opacity="0.1"/>
    <SolidColorBrush x:Key="HoverBrush" Color="{StaticResource PrimaryColor}" Opacity="0.08"/>

    <!-- 漸層筆刷 -->
    <LinearGradientBrush x:Key="HeaderGradientBrush" StartPoint="0,0" EndPoint="0,1">
        <GradientStop Color="{StaticResource PrimaryColor}" Offset="0"/>
        <GradientStop Color="{StaticResource PrimaryDarkColor}" Offset="1"/>
    </LinearGradientBrush>

    <!-- 陰影筆刷（使用 DropShadowEffect） -->
    <DropShadowEffect x:Key="ElevationShadow1"
                      BlurRadius="4"
                      ShadowDepth="1"
                      Direction="270"
                      Color="#000000"
                      Opacity="0.2"/>

    <DropShadowEffect x:Key="ElevationShadow2"
                      BlurRadius="8"
                      ShadowDepth="2"
                      Direction="270"
                      Color="#000000"
                      Opacity="0.24"/>

    <DropShadowEffect x:Key="ElevationShadow3"
                      BlurRadius="16"
                      ShadowDepth="4"
                      Direction="270"
                      Color="#000000"
                      Opacity="0.3"/>
</ResourceDictionary>
```

### 字體系統

```xml
<!-- Resources/Fonts.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <!-- 字體家族 -->
    <FontFamily x:Key="PrimaryFont">Segoe UI</FontFamily>
    <FontFamily x:Key="DisplayFont">Segoe UI Semibold</FontFamily>
    <FontFamily x:Key="MonospaceFont">Consolas</FontFamily>

    <!-- 字體大小 - 使用 Type Scale -->
    <system:Double x:Key="FontSize10">10</system:Double>
    <system:Double x:Key="FontSize12">12</system:Double>
    <system:Double x:Key="FontSize14">14</system:Double>
    <system:Double x:Key="FontSize16">16</system:Double>
    <system:Double x:Key="FontSize18">18</system:Double>
    <system:Double x:Key="FontSize20">20</system:Double>
    <system:Double x:Key="FontSize24">24</system:Double>
    <system:Double x:Key="FontSize32">32</system:Double>
    <system:Double x:Key="FontSize48">48</system:Double>

    <!-- 字體粗細 -->
    <FontWeight x:Key="FontWeightLight">Light</FontWeight>
    <FontWeight x:Key="FontWeightRegular">Normal</FontWeight>
    <FontWeight x:Key="FontWeightMedium">Medium</FontWeight>
    <FontWeight x:Key="FontWeightSemiBold">SemiBold</FontWeight>
    <FontWeight x:Key="FontWeightBold">Bold</FontWeight>

    <!-- 文字樣式 -->
    <Style x:Key="Heading1" TargetType="TextBlock">
        <Setter Property="FontFamily" Value="{StaticResource DisplayFont}"/>
        <Setter Property="FontSize" Value="{StaticResource FontSize32}"/>
        <Setter Property="FontWeight" Value="{StaticResource FontWeightSemiBold}"/>
        <Setter Property="Foreground" Value="{StaticResource PrimaryBrush}"/>
    </Style>

    <Style x:Key="Heading2" TargetType="TextBlock">
        <Setter Property="FontFamily" Value="{StaticResource DisplayFont}"/>
        <Setter Property="FontSize" Value="{StaticResource FontSize24}"/>
        <Setter Property="FontWeight" Value="{StaticResource FontWeightMedium}"/>
    </Style>

    <Style x:Key="Body1" TargetType="TextBlock">
        <Setter Property="FontFamily" Value="{StaticResource PrimaryFont}"/>
        <Setter Property="FontSize" Value="{StaticResource FontSize14}"/>
        <Setter Property="FontWeight" Value="{StaticResource FontWeightRegular}"/>
    </Style>

    <Style x:Key="Caption" TargetType="TextBlock">
        <Setter Property="FontFamily" Value="{StaticResource PrimaryFont}"/>
        <Setter Property="FontSize" Value="{StaticResource FontSize12}"/>
        <Setter Property="Foreground" Value="{DynamicResource TextSecondaryBrush}"/>
    </Style>
</ResourceDictionary>
```

---

## 🎭 控制項樣式設計

### 現代化按鈕樣式

```xml
<!-- Resources/Styles/ButtonStyles.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <!-- 扁平化主要按鈕 -->
    <Style x:Key="PrimaryButton" TargetType="Button">
        <Setter Property="Background" Value="{StaticResource PrimaryBrush}"/>
        <Setter Property="Foreground" Value="White"/>
        <Setter Property="BorderThickness" Value="0"/>
        <Setter Property="Padding" Value="16,8"/>
        <Setter Property="FontSize" Value="{StaticResource FontSize14}"/>
        <Setter Property="FontWeight" Value="{StaticResource FontWeightMedium}"/>
        <Setter Property="Cursor" Value="Hand"/>
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="Button">
                    <Border x:Name="border"
                            Background="{TemplateBinding Background}"
                            BorderBrush="{TemplateBinding BorderBrush}"
                            BorderThickness="{TemplateBinding BorderThickness}"
                            CornerRadius="4"
                            SnapsToDevicePixels="True">
                        <ContentPresenter HorizontalAlignment="Center"
                                        VerticalAlignment="Center"
                                        Margin="{TemplateBinding Padding}"/>
                    </Border>
                    <ControlTemplate.Triggers>
                        <!-- Hover 效果 -->
                        <Trigger Property="IsMouseOver" Value="True">
                            <Setter TargetName="border" Property="Background"
                                    Value="{StaticResource PrimaryLightBrush}"/>
                            <Setter TargetName="border" Property="Effect">
                                <Setter.Value>
                                    <DropShadowEffect BlurRadius="8"
                                                    ShadowDepth="2"
                                                    Color="#000000"
                                                    Opacity="0.3"/>
                                </Setter.Value>
                            </Setter>
                        </Trigger>

                        <!-- Pressed 效果 -->
                        <Trigger Property="IsPressed" Value="True">
                            <Setter TargetName="border" Property="Background"
                                    Value="{StaticResource PrimaryDarkBrush}"/>
                            <Setter TargetName="border" Property="Effect" Value="{x:Null}"/>
                        </Trigger>

                        <!-- Disabled 效果 -->
                        <Trigger Property="IsEnabled" Value="False">
                            <Setter TargetName="border" Property="Background"
                                    Value="{StaticResource DisabledBrush}"/>
                            <Setter TargetName="border" Property="Opacity" Value="0.5"/>
                        </Trigger>
                    </ControlTemplate.Triggers>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
    </Style>

    <!-- Outlined 按鈕 -->
    <Style x:Key="OutlinedButton" TargetType="Button">
        <Setter Property="Background" Value="Transparent"/>
        <Setter Property="Foreground" Value="{StaticResource PrimaryBrush}"/>
        <Setter Property="BorderBrush" Value="{StaticResource PrimaryBrush}"/>
        <Setter Property="BorderThickness" Value="1"/>
        <Setter Property="Padding" Value="16,8"/>
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="Button">
                    <Border x:Name="border"
                            Background="{TemplateBinding Background}"
                            BorderBrush="{TemplateBinding BorderBrush}"
                            BorderThickness="{TemplateBinding BorderThickness}"
                            CornerRadius="4">
                        <ContentPresenter HorizontalAlignment="Center"
                                        VerticalAlignment="Center"
                                        Margin="{TemplateBinding Padding}"/>
                    </Border>
                    <ControlTemplate.Triggers>
                        <Trigger Property="IsMouseOver" Value="True">
                            <Setter TargetName="border" Property="Background"
                                    Value="{StaticResource HoverBrush}"/>
                        </Trigger>
                        <Trigger Property="IsPressed" Value="True">
                            <Setter TargetName="border" Property="Background"
                                    Value="{StaticResource OverlayBrush}"/>
                        </Trigger>
                    </ControlTemplate.Triggers>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
    </Style>

    <!-- Icon 按鈕 -->
    <Style x:Key="IconButton" TargetType="Button">
        <Setter Property="Background" Value="Transparent"/>
        <Setter Property="BorderThickness" Value="0"/>
        <Setter Property="Width" Value="40"/>
        <Setter Property="Height" Value="40"/>
        <Setter Property="Cursor" Value="Hand"/>
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="Button">
                    <Border x:Name="border"
                            Background="{TemplateBinding Background}"
                            CornerRadius="20">
                        <ContentPresenter HorizontalAlignment="Center"
                                        VerticalAlignment="Center"/>
                    </Border>
                    <ControlTemplate.Triggers>
                        <Trigger Property="IsMouseOver" Value="True">
                            <Setter TargetName="border" Property="Background"
                                    Value="{StaticResource HoverBrush}"/>
                        </Trigger>
                        <Trigger Property="IsPressed" Value="True">
                            <Setter TargetName="border" Property="Background"
                                    Value="{StaticResource OverlayBrush}"/>
                        </Trigger>
                    </ControlTemplate.Triggers>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
    </Style>
</ResourceDictionary>
```

### 現代化 TextBox 樣式

```xml
<!-- 浮動標籤 TextBox -->
<Style x:Key="FloatingLabelTextBox" TargetType="TextBox">
    <Setter Property="Height" Value="56"/>
    <Setter Property="Padding" Value="16,20,16,8"/>
    <Setter Property="FontSize" Value="{StaticResource FontSize14}"/>
    <Setter Property="BorderBrush" Value="{StaticResource BorderBrush}"/>
    <Setter Property="BorderThickness" Value="0,0,0,1"/>
    <Setter Property="Background" Value="{StaticResource SurfaceBrush}"/>
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="TextBox">
                <Grid>
                    <Border x:Name="border"
                            Background="{TemplateBinding Background}"
                            BorderBrush="{TemplateBinding BorderBrush}"
                            BorderThickness="{TemplateBinding BorderThickness}"
                            CornerRadius="4,4,0,0">
                        <Grid>
                            <!-- 浮動標籤 -->
                            <TextBlock x:Name="floatingLabel"
                                      Text="{TemplateBinding Tag}"
                                      FontSize="12"
                                      Foreground="{StaticResource TextSecondaryBrush}"
                                      Margin="16,8,16,0"
                                      VerticalAlignment="Top"
                                      IsHitTestVisible="False"/>

                            <!-- 輸入框 -->
                            <ScrollViewer x:Name="PART_ContentHost"
                                        Margin="{TemplateBinding Padding}"
                                        VerticalAlignment="Center"/>

                            <!-- Placeholder -->
                            <TextBlock x:Name="placeholder"
                                      Text="{TemplateBinding Tag}"
                                      Foreground="{StaticResource TextSecondaryBrush}"
                                      Margin="{TemplateBinding Padding}"
                                      VerticalAlignment="Center"
                                      IsHitTestVisible="False">
                                <TextBlock.Style>
                                    <Style TargetType="TextBlock">
                                        <Setter Property="Visibility" Value="Collapsed"/>
                                        <Style.Triggers>
                                            <DataTrigger Binding="{Binding Text.Length, RelativeSource={RelativeSource TemplatedParent}}" Value="0">
                                                <Setter Property="Visibility" Value="Visible"/>
                                            </DataTrigger>
                                        </Style.Triggers>
                                    </Style>
                                </TextBlock.Style>
                            </TextBlock>
                        </Grid>
                    </Border>

                    <!-- Focus Indicator -->
                    <Border x:Name="focusIndicator"
                            Height="2"
                            VerticalAlignment="Bottom"
                            Background="{StaticResource PrimaryBrush}"
                            Opacity="0"/>
                </Grid>

                <ControlTemplate.Triggers>
                    <!-- 有文字時隱藏 placeholder，顯示浮動標籤 -->
                    <Trigger Property="Text" Value="">
                        <Setter TargetName="floatingLabel" Property="Visibility" Value="Collapsed"/>
                    </Trigger>

                    <!-- Focus 效果 -->
                    <Trigger Property="IsFocused" Value="True">
                        <Setter TargetName="focusIndicator" Property="Opacity" Value="1"/>
                        <Setter TargetName="floatingLabel" Property="Foreground"
                                Value="{StaticResource PrimaryBrush}"/>
                        <Trigger.EnterActions>
                            <BeginStoryboard>
                                <Storyboard>
                                    <DoubleAnimation Storyboard.TargetName="focusIndicator"
                                                   Storyboard.TargetProperty="Opacity"
                                                   To="1"
                                                   Duration="0:0:0.2"/>
                                </Storyboard>
                            </BeginStoryboard>
                        </Trigger.EnterActions>
                        <Trigger.ExitActions>
                            <BeginStoryboard>
                                <Storyboard>
                                    <DoubleAnimation Storyboard.TargetName="focusIndicator"
                                                   Storyboard.TargetProperty="Opacity"
                                                   To="0"
                                                   Duration="0:0:0.2"/>
                                </Storyboard>
                            </BeginStoryboard>
                        </Trigger.ExitActions>
                    </Trigger>
                </ControlTemplate.Triggers>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
```

---

## 🎬 動畫與轉場

### 頁面轉場動畫

```xml
<!-- 淡入淡出轉場 -->
<Storyboard x:Key="FadeInAnimation">
    <DoubleAnimation Storyboard.TargetProperty="Opacity"
                     From="0" To="1"
                     Duration="0:0:0.3">
        <DoubleAnimation.EasingFunction>
            <CubicEase EasingMode="EaseOut"/>
        </DoubleAnimation.EasingFunction>
    </DoubleAnimation>
</Storyboard>

<!-- 滑入動畫 -->
<Storyboard x:Key="SlideInFromRightAnimation">
    <DoubleAnimation Storyboard.TargetProperty="(UIElement.RenderTransform).(TranslateTransform.X)"
                     From="50" To="0"
                     Duration="0:0:0.4">
        <DoubleAnimation.EasingFunction>
            <CubicEase EasingMode="EaseOut"/>
        </DoubleAnimation.EasingFunction>
    </DoubleAnimation>
    <DoubleAnimation Storyboard.TargetProperty="Opacity"
                     From="0" To="1"
                     Duration="0:0:0.3"/>
</Storyboard>
```

### 載入動畫

```xml
<!-- 旋轉載入指示器 -->
<Style x:Key="LoadingSpinner" TargetType="Control">
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="Control">
                <Viewbox Width="40" Height="40">
                    <Canvas Width="40" Height="40">
                        <Path Data="M 20,4 A 16,16 0 1 1 19.999,4"
                              Stroke="{StaticResource PrimaryBrush}"
                              StrokeThickness="4"
                              StrokeDashArray="25,75"
                              StrokeLineCap="Round">
                            <Path.RenderTransform>
                                <RotateTransform CenterX="20" CenterY="20"/>
                            </Path.RenderTransform>
                            <Path.Triggers>
                                <EventTrigger RoutedEvent="Loaded">
                                    <BeginStoryboard>
                                        <Storyboard RepeatBehavior="Forever">
                                            <DoubleAnimation Storyboard.TargetProperty="(Path.RenderTransform).(RotateTransform.Angle)"
                                                           From="0" To="360"
                                                           Duration="0:0:1"/>
                                        </Storyboard>
                                    </BeginStoryboard>
                                </EventTrigger>
                            </Path.Triggers>
                        </Path>
                    </Canvas>
                </Viewbox>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
```

---

## 🌓 主題切換系統

### 動態主題管理器

```csharp
// Services/ThemeManager.cs
public class ThemeManager
{
    private static ThemeManager? _instance;
    public static ThemeManager Instance => _instance ??= new ThemeManager();

    public enum Theme
    {
        Light,
        Dark,
        System
    }

    private Theme _currentTheme = Theme.System;

    public void ApplyTheme(Theme theme)
    {
        _currentTheme = theme;

        var themeName = theme == Theme.Dark ? "DarkTheme" : "LightTheme";

        var themeUri = new Uri($"Resources/Themes/{themeName}.xaml", UriKind.Relative);
        var themeDict = new ResourceDictionary { Source = themeUri };

        Application.Current.Resources.MergedDictionaries.Clear();
        Application.Current.Resources.MergedDictionaries.Add(themeDict);
    }

    public Theme CurrentTheme => _currentTheme;
}
```

### 主題資源字典

```xml
<!-- Resources/Themes/LightTheme.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <SolidColorBrush x:Key="BackgroundBrush" Color="#FFFFFF"/>
    <SolidColorBrush x:Key="SurfaceBrush" Color="#F5F5F5"/>
    <SolidColorBrush x:Key="TextPrimaryBrush" Color="#212121"/>
    <SolidColorBrush x:Key="TextSecondaryBrush" Color="#757575"/>

    <!-- 合併其他資源 -->
    <ResourceDictionary.MergedDictionaries>
        <ResourceDictionary Source="../Colors.xaml"/>
        <ResourceDictionary Source="../Brushes.xaml"/>
        <ResourceDictionary Source="../Fonts.xaml"/>
    </ResourceDictionary.MergedDictionaries>
</ResourceDictionary>

<!-- Resources/Themes/DarkTheme.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <SolidColorBrush x:Key="BackgroundBrush" Color="#121212"/>
    <SolidColorBrush x:Key="SurfaceBrush" Color="#1E1E1E"/>
    <SolidColorBrush x:Key="TextPrimaryBrush" Color="#FFFFFF"/>
    <SolidColorBrush x:Key="TextSecondaryBrush" Color="#B0B0B0"/>

    <!-- 合併其他資源 -->
    <ResourceDictionary.MergedDictionaries>
        <ResourceDictionary Source="../Colors.xaml"/>
        <ResourceDictionary Source="../Brushes.xaml"/>
        <ResourceDictionary Source="../Fonts.xaml"/>
    </ResourceDictionary.MergedDictionaries>
</ResourceDictionary>
```

---

## 🎨 Material Design Integration

### 使用 MaterialDesignThemes

```xml
<!-- 安裝 NuGet 套件 -->
<!-- MaterialDesignThemes -->

<!-- App.xaml -->
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.MergedDictionaries>
            <!-- Material Design -->
            <materialDesign:BundledTheme BaseTheme="Light"
                                        PrimaryColor="Blue"
                                        SecondaryColor="Orange"/>
            <ResourceDictionary Source="pack://application:,,,/MaterialDesignThemes.Wpf;component/Themes/MaterialDesignTheme.Defaults.xaml"/>

            <!-- 自訂資源 -->
            <ResourceDictionary Source="Resources/Colors.xaml"/>
        </ResourceDictionary.MergedDictionaries>
    </ResourceDictionary>
</Application.Resources>
```

### Material Design 元件範例

```xml
<!-- Card -->
<materialDesign:Card Padding="16" Margin="8">
    <StackPanel>
        <TextBlock Style="{StaticResource MaterialDesignHeadline6TextBlock}"
                   Text="Card Title"/>
        <TextBlock Style="{StaticResource MaterialDesignBody2TextBlock}"
                   Text="Card content goes here"
                   TextWrapping="Wrap"
                   Margin="0,8"/>
    </StackPanel>
</materialDesign:Card>

<!-- Floating Action Button -->
<Button Style="{StaticResource MaterialDesignFloatingActionButton}"
        Command="{Binding AddCommand}">
    <materialDesign:PackIcon Kind="Plus"/>
</Button>

<!-- Snackbar 通知 -->
<materialDesign:Snackbar x:Name="Snackbar"
                        MessageQueue="{Binding MessageQueue}"/>
```

---

## 🖼️ 自訂控制項範例

### 卡片控制項

```csharp
// Controls/Card.cs
public class Card : ContentControl
{
    static Card()
    {
        DefaultStyleKeyProperty.OverrideMetadata(
            typeof(Card),
            new FrameworkPropertyMetadata(typeof(Card)));
    }

    public static readonly DependencyProperty ElevationProperty =
        DependencyProperty.Register(nameof(Elevation), typeof(int), typeof(Card),
            new PropertyMetadata(1, OnElevationChanged));

    public int Elevation
    {
        get => (int)GetValue(ElevationProperty);
        set => SetValue(ElevationProperty, value);
    }

    private static void OnElevationChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is Card card)
        {
            var elevation = (int)e.NewValue;
            card.Effect = elevation switch
            {
                1 => Application.Current.FindResource("ElevationShadow1") as Effect,
                2 => Application.Current.FindResource("ElevationShadow2") as Effect,
                3 => Application.Current.FindResource("ElevationShadow3") as Effect,
                _ => null
            };
        }
    }
}
```

```xml
<!-- Themes/Generic.xaml -->
<Style TargetType="local:Card">
    <Setter Property="Background" Value="{DynamicResource SurfaceBrush}"/>
    <Setter Property="Padding" Value="16"/>
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="local:Card">
                <Border Background="{TemplateBinding Background}"
                        CornerRadius="8"
                        Padding="{TemplateBinding Padding}">
                    <ContentPresenter/>
                </Border>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
```

---

## 💡 最佳實踐

### 1. 資源管理

- ✅ 使用 `StaticResource` 而非 `DynamicResource`（效能更好）
- ✅ 將資源組織到邏輯分類的檔案中
- ✅ 使用有意義的 `x:Key` 名稱
- ❌ 避免在 XAML 中直接定義顏色值

### 2. 效能優化

- ✅ 避免過度使用 `DropShadowEffect`（耗效能）
- ✅ 使用 `Freeze()` 凍結不變的資源
- ✅ 避免深層巢狀的視覺樹
- ✅ 使用虛擬化（VirtualizingStackPanel）處理大量項目

### 3. 響應式設計

- ✅ 使用 `Grid` 而非固定大小
- ✅ 支援不同 DPI 縮放
- ✅ 測試不同解析度

### 4. 可存取性

- ✅ 設定 `AutomationProperties.Name`
- ✅ 確保色彩對比度
- ✅ 支援高對比度模式
- ✅ 完整的鍵盤導航

---

## 🎯 專案特定範例

### 專案中的實際應用

基於此專案的需求，以下是具體建議：

#### 1. 暫存器視圖的卡片化

```xml
<!-- 將暫存器組顯示為卡片 -->
<ItemsControl ItemsSource="{Binding Registers}">
    <ItemsControl.ItemsPanel>
        <ItemsPanelTemplate>
            <WrapPanel Orientation="Horizontal"/>
        </ItemsPanelTemplate>
    </ItemsControl.ItemsPanel>
    <ItemsControl.ItemTemplate>
        <DataTemplate>
            <local:Card Elevation="1" Margin="8" Width="200">
                <StackPanel>
                    <TextBlock Text="{Binding Name}"
                               Style="{StaticResource Heading2}"/>
                    <TextBlock Text="{Binding Address, StringFormat=0x{0:X4}}"
                               Style="{StaticResource Caption}"/>
                    <TextBox Text="{Binding Value}"
                             Style="{StaticResource FloatingLabelTextBox}"
                             Tag="Value"
                             Margin="0,8,0,0"/>
                </StackPanel>
            </local:Card>
        </DataTemplate>
    </ItemsControl.ItemTemplate>
</ItemsControl>
```

#### 2. 狀態指示器

```xml
<!-- 連線狀態指示 -->
<Border Background="{StaticResource SuccessBrush}"
        CornerRadius="10"
        Padding="8,4"
        Visibility="{Binding IsConnected, Converter={StaticResource BoolToVisibilityConverter}}">
    <StackPanel Orientation="Horizontal">
        <Ellipse Width="8" Height="8" Fill="White" Margin="0,0,4,0"/>
        <TextBlock Text="Connected" Foreground="White" FontSize="12"/>
    </StackPanel>
</Border>
```

#### 3. 資料載入覆蓋層

```xml
<!-- 載入中覆蓋 -->
<Grid Visibility="{Binding IsLoading, Converter={StaticResource BoolToVisibilityConverter}}">
    <Border Background="#80000000"/>
    <StackPanel HorizontalAlignment="Center" VerticalAlignment="Center">
        <Control Style="{StaticResource LoadingSpinner}"/>
        <TextBlock Text="Loading..."
                   Foreground="White"
                   FontSize="16"
                   Margin="0,16,0,0"
                   HorizontalAlignment="Center"/>
    </StackPanel>
</Grid>
```

---

## 📋 檢查清單

完成 WPF 前端設計後驗證：

### 視覺設計

- [ ] 定義完整的色彩系統（Primary、Accent、Semantic）
- [ ] 建立字體階層（Heading、Body、Caption）
- [ ] 設計一致的間距系統
- [ ] 實作陰影/深度系統

### 控制項樣式

- [ ] 自訂所有主要控制項樣式
- [ ] 實作 Hover、Pressed、Disabled 狀態
- [ ] 添加適當的動畫轉場
- [ ] 支援深色模式

### 效能

- [ ] 避免過度使用 Effect
- [ ] 使用 StaticResource
- [ ] 虛擬化長列表
- [ ] 測試不同 DPI 下的效能

### 可存取性

- [ ] 鍵盤完整可操作
- [ ] AutomationProperties 設定
- [ ] 色彩對比度檢查
- [ ] 高對比度模式支援

---

**版本**：1.0
**最後更新**：2026-01-19
**專注領域**：WPF 桌面應用程式的現代化 UI/UX 設計
