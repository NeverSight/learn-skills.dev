---
name: flutter-infinite-canvas
description: Learn how to build an infinite, multi-touch canvas in Flutter using InteractiveViewer and CustomMultiChildLayout for a flexible and interactive user experience.
metadata:
  url: https://rodydavis.com/posts/snippets/flutter-infinite-canvas
  last_modified: Tue, 03 Feb 2026 20:04:31 GMT
---

# Flutter Infinite Canvas


## Overview 

The following is an example of how to build an infinite canvas with [InteractiveViewer](https://api.flutter.dev/flutter/widgets/InteractiveViewer-class.html) and [CustomMultiChildLayout](https://api.flutter.dev/flutter/widgets/CustomMultiChildLayout-class.html).

Blog post: [Create a multi touch canvas in Flutter](https://rodydavis.com/posts/flutter-multi-touch-canvas)

```
import 'package:flutter/material.dart';
import 'package:vector_math/vector_math_64.dart' hide Colors;

void main() {
  final controller = WidgetCanvasController([
    WidgetCanvasChild(
      key: UniqueKey(),
      offset: Offset.zero,
      size: const Size(400, 800),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Scaffold 1'),
        ),
        body: const Placeholder(),
      ),
    ),
    WidgetCanvasChild(
      key: UniqueKey(),
      offset: const Offset(200, 200),
      size: const Size(400, 800),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Scaffold 2'),
        ),
        body: const Placeholder(),
      ),
    ),
  ]);
  runApp(MaterialApp(home: WidgetCanvas(controller: controller)));
}

class WidgetCanvas extends StatefulWidget {
  const WidgetCanvas({super.key, required this.controller});

  final WidgetCanvasController controller;

  @override
  State<WidgetCanvas> createState() => WidgetCanvasState();
}

class WidgetCanvasState extends State<WidgetCanvas> {
  @override
  void initState() {
    super.initState();
    controller.addListener(onUpdate);
  }

  @override
  void dispose() {
    controller.removeListener(onUpdate);
    super.dispose();
  }

  void onUpdate() {
    if (mounted) setState(() {});
  }

  static const Size _gridSize = Size.square(50);
  WidgetCanvasController get controller => widget.controller;

  Rect axisAlignedBoundingBox(Quad quad) {
    double xMin = quad.point0.x;
    double xMax = quad.point0.x;
    double yMin = quad.point0.y;
    double yMax = quad.point0.y;
    for (final Vector3 point in <Vector3>[
      quad.point1,
      quad.point2,
      quad.point3,
    ]) {
      if (point.x < xMin) {
        xMin = point.x;
      } else if (point.x > xMax) {
        xMax = point.x;
      }

      if (point.y < yMin) {
        yMin = point.y;
      } else if (point.y > yMax) {
        yMax = point.y;
      }
    }

    return Rect.fromLTRB(xMin, yMin, xMax, yMax);
  }

  @override
  Widget build(BuildContext context) {
    const inset = 2.0;
    return Listener(
      onPointerDown: (details) {
        controller.mouseDown = true;
        controller.checkSelection(details.localPosition);
      },
      onPointerUp: (details) {
        controller.mouseDown = false;
      },
      onPointerCancel: (details) {
        controller.mouseDown = false;
      },
      onPointerMove: (details) {},
      child: LayoutBuilder(
        builder: (context, constraints) => InteractiveViewer.builder(
          transformationController: controller.transform,
          panEnabled: controller.canvasMoveEnabled,
          scaleEnabled: controller.canvasMoveEnabled,
          onInteractionStart: (details) {
            controller.mousePosition = details.focalPoint;
          },
          onInteractionUpdate: (details) {
            if (!controller.mouseDown) {
              controller.scale = details.scale;
            } else {
              controller.moveSelection(details.focalPoint);
            }
            controller.mousePosition = details.focalPoint;
          },
          onInteractionEnd: (details) {},
          minScale: 0.4,
          maxScale: 4,
          boundaryMargin: const EdgeInsets.all(double.infinity),
          builder: (context, viewport) {
            return SizedBox(
              width: 1,
              height: 1,
              child: Stack(
                clipBehavior: Clip.none,
                children: [
                  Positioned.fill(
                    child: GridBackgroundBuilder(
                      cellWidth: _gridSize.width,
                      cellHeight: _gridSize.height,
                      viewport: axisAlignedBoundingBox(viewport),
                    ),
                  ),
                  Positioned.fill(
                    child: CustomMultiChildLayout(
                      delegate: WidgetCanvasDelegate(controller),
                      children: controller.children.map((e) {
                        return LayoutId(
                            id: e,
                            child: Stack(
                              clipBehavior: Clip.none,
                              children: [
                                Positioned.fill(
                                  child: Material(
                                    elevation: 4,
                                    child: SizedBox.fromSize(
                                      size: e.size,
                                      child: e.child,
                                    ),
                                  ),
                                ),
                                if (controller.isSelected(e.key!))
                                  Positioned.fill(
                                    top: -inset,
                                    left: -inset,
                                    right: -inset,
                                    bottom: -inset,
                                    child: Container(
                                      decoration: BoxDecoration(
                                        border: Border.all(
                                          color: Colors.blue,
                                          width: 1,
                                        ),
                                      ),
                                    ),
                                  ),
                              ],
                            ));
                      }).toList(),
                    ),
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}

class GridBackgroundBuilder extends StatelessWidget {
  const GridBackgroundBuilder({
    super.key,
    required this.cellWidth,
    required this.cellHeight,
    required this.viewport,
  });

  final double cellWidth;
  final double cellHeight;
  final Rect viewport;

  @override
  Widget build(BuildContext context) {
    final int firstRow = (viewport.top / cellHeight).floor();
    final int lastRow = (viewport.bottom / cellHeight).ceil();
    final int firstCol = (viewport.left / cellWidth).floor();
    final int lastCol = (viewport.right / cellWidth).ceil();

    return Stack(
      clipBehavior: Clip.none,
      children: <Widget>[
        for (int row = firstRow; row < lastRow; row++)
          for (int col = firstCol; col < lastCol; col++)
            Positioned(
              left: col * cellWidth,
              top: row * cellHeight,
              child: Container(
                height: cellHeight,
                width: cellWidth,
                decoration: BoxDecoration(
                  border: Border.all(
                    color: Colors.grey.withOpacity(0.1),
                    width: 1,
                  ),
                ),
              ),
            ),
      ],
    );
  }
}

class WidgetCanvasDelegate extends MultiChildLayoutDelegate {
  WidgetCanvasDelegate(this.controller);
  final WidgetCanvasController controller;
  List<WidgetCanvasChild> get children => controller.children;

  Size backgroundSize = const Size(100000, 100000);
  late Offset backgroundOffset = Offset(
    -backgroundSize.width / 2,
    -backgroundSize.height / 2,
  );

  @override
  void performLayout(Size size) {
    // Then draw the screens.
    for (final widget in children) {
      layoutChild(widget, BoxConstraints.tight(widget.size));
      positionChild(widget, widget.offset);
    }
  }

  @override
  bool shouldRelayout(WidgetCanvasDelegate oldDelegate) => true;
}

class WidgetCanvasChild extends StatelessWidget {
  const WidgetCanvasChild({
    required Key key,
    required this.size,
    required this.offset,
    required this.child,
  }) : super(key: key);

  final Size size;
  final Offset offset;
  final Widget child;

  Rect get rect => offset & size;

  WidgetCanvasChild copyWith({
    Size? size,
    Offset? offset,
    Widget? child,
  }) {
    return WidgetCanvasChild(
      key: key!,
      size: size ?? this.size,
      offset: offset ?? this.offset,
      child: child ?? this.child,
    );
  }

  @override
  Widget build(BuildContext context) {
    return child;
  }
}

class WidgetCanvasController extends ChangeNotifier {
  WidgetCanvasController(this.children);

  final List<WidgetCanvasChild> children;
  final Set<Key> _selected = {};
  late final transform = TransformationController();
  Matrix4 get matrix => transform.value;
  double scale = 1;
  Offset mousePosition = Offset.zero;

  bool _mouseDown = false;
  bool get mouseDown => _mouseDown;
  set mouseDown(bool value) {
    _mouseDown = value;
    notifyListeners();
  }

  bool isSelected(Key key) => _selected.contains(key);

  bool get hasSelection => _selected.isNotEmpty;

  bool get canvasMoveEnabled => !mouseDown;

  Offset toLocal(Offset global) {
    return transform.toScene(global);
  }

  void checkSelection(Offset localPosition) {
    final offset = toLocal(localPosition);
    final selection = <Key>[];
    for (final child in children) {
      final rect = child.rect;
      if (rect.contains(offset)) {
        selection.add(child.key!);
      }
    }
    if (selection.isNotEmpty) {
      setSelection({selection.last});
    } else {
      deselectAll();
    }
  }

  void moveSelection(Offset position) {
    final delta = toLocal(position) - toLocal(mousePosition);
    for (final key in _selected) {
      final index = children.indexWhere((e) => e.key == key);
      if (index == -1) continue;
      final current = children[index];
      children[index] = current.copyWith(
        offset: current.offset + delta,
      );
    }
    mousePosition = position;
    notifyListeners();
  }

  void select(Key key) {
    _selected.add(key);
    notifyListeners();
  }

  void setSelection(Set<Key> keys) {
    _selected.clear();
    _selected.addAll(keys);
    notifyListeners();
  }

  void deselect(Key key) {
    _selected.remove(key);
    notifyListeners();
  }

  void deselectAll() {
    _selected.clear();
    notifyListeners();
  }

  void add(WidgetCanvasChild child) {
    children.add(child);
    notifyListeners();
  }

  void remove(Key key) {
    children.removeWhere((e) => e.key == key);
    notifyListeners();
  }
}
```

## Demo