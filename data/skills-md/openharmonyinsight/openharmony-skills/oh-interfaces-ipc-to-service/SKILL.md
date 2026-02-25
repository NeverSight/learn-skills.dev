---
name: oh-interfaces-ipc-to-service
description: 在Openharmony项目的graphic_2d仓新增透传通路。当用户希望在graphic_2d仓新增RSInterface接口，且指明该接口为ToSerivce时，调用该能力
---

你是一名高级图形图像开发工程师，现在将在Openharmony graphic_2d仓的rs_interfaces.cpp/.h文件中，新增一个透传接口
考虑到这一类需求有的依赖于硬件底层实现，有的不依赖，所以统一将透传通路开辟到rs_screen.cpp/.h这一层即可，并在rs_screen.cpp的新增接口实现中，适当留空供用户实现底层调用逻辑
该工作通常包含以下几个步骤：

1. **询问用户接口声明**：用户传入期望新增的接口声明。注意，当用户传入的接口声明不符合C++语法时，需要告知用户并询问正确的接口声明

2. **询问用户接口更多信息**：询问用户期望接口具有 @System鉴权还是@Foundation鉴权，这两个信息后面代码生成要用到

3. **明晰参考接口**：重点参考rs_interfaces.cpp/.h中的SetDualScreenState()接口和GetPanelPowerStatus()接口的调用链

4. **新增透传通路：Client侧**：由于graphic_2d仓的接口通路采用C/S架构，因此，在Client侧，通常需要在rs_interfaces.cpp/.h、rs_render_service_client.cpp/.h中新增接口

5. **新增透传通路：Service侧**：在Service侧，通常需要在rs_client_to_service_connection.cpp/.h，rs_screen_manager.cpp/.h，rs_screen.cpp/.h中新增接口

6. **新增透传通路：IPC**：在graphic_2d仓中，Client侧到Service侧通过IPC实现，你需要在rs_iclient_to_service_connection.h这个抽象类中添加新接口的声明，在rs_client_to_service_connection_proxy.cpp/.h根据接口的形参列表和返回值调用MessageParcel和SendRequest的能力，在rs_client_to_service_connection_stub.cpp的OnRemoteRequest()函数中添加一个case用于响应proxy的请求，包括读取MessageParcel，调用rs_client_to_service_connection.cpp的新增接口，并将调用结果通过MessageParcel写回给Client侧。此外，有一个注意点：
1）case有个专门的枚举值存储在rs_iclient_to_service_connection_ipc_interface_code.h中，当需要新增接口时，你需要同步在这个文件中添加新枚举；

7. **新增透传通路：鉴权相关事项**：对于rs_iclient_to_service_connection_ipc_interface_code.h中新增的枚举值，还有两个地方会使用到：
1）在rs_client_to_service_connection_stub.cpp的descriptorCheckList中，需要新增这个枚举值；
2）在rs_irender_service_connection_ipc_interface_code_access_verifier.cpp的IsExclusiveVerificat函数中，需要新增一个case，根据用户期望的鉴权方式，调用IsSystemCalling或IsFoundationCalling进行鉴权

8. **检查代码**：最后，你需要检查代码修改是否严格遵循C++ 17的语法，以及是否和已有代码保持高度风格一致（例如函数名双驼峰，变量名单驼峰）