### Intrduction
painlessMesh is a library that takes care of the particulars of creating a simple mesh network using esp8266 and esp32 hardware.  The goal is to allow the programmer to work with a mesh network without having to worry about how the network is structured or managed.

### True ad-hoc networking

painlessMesh is a true ad-hoc network, meaning that no-planning, central controller, or router is required.  Any system of 1 or more nodes will self-organize into fully functional mesh.  The maximum size of the mesh is limited (we think) by the amount of memory in the heap that can be allocated to the sub-connections buffer and so should be really quite high.

### JSON based

painlessMesh uses JSON objects for all its messaging.  There are a couple of reasons for this.  First, it makes the code and the messages human readable and painless to understand and second, it makes it painless to integrate painlessMesh with javascript front-ends, web applications, and other apps.  Some performance is lost, but I haven’t been running into performance issues yet.  Converting to binary messaging would be fairly straight forward if someone wants to contribute.

### Wifi &amp; Networking

painlessMesh is designed to be used with Arduino, but it does not use the Arduino WiFi libraries, as we were running into performance issues (primarily latency) with them.  Rather the networking is all done using the native esp32 and esp8266 SDK libraries, which are available through the Arduino IDE.  Hopefully though, which networking libraries are used won’t matter to most users much as you can just include painlessMesh.h, run the init() and then work the library through the API.

### painlessMesh is not IP networking

painlessMesh does not create a TCP/IP network of nodes. Rather each of the nodes is uniquely identified by its 32bit chipId which is retrieved from the esp8266/esp32 using the `system_get_chip_id()` call in the SDK.  Every node will have a unique number.  Messages can either be broadcast to all of the nodes on the mesh, or sent specifically to an individual node which is identified by its `nodeId.

### Limitations and caveats

- Try to avoid using `delay()` in your code. To maintain the mesh we need to perform some tasks in the background. Using `delay()` will stop these tasks from happening and can cause the mesh to lose stability/fall apart. Instead we recommend using [TaskScheduler](http://playground.arduino.cc/Code/TaskScheduler) which is used in `painlessMesh` itself. Documentation can be found [here](https://github.com/arkhipenko/TaskScheduler/wiki/Full-Document). For other examples on how to use the scheduler see the example folder.
- `painlessMesh` subscribes to WiFi events. Please be aware that as a result `painlessMesh` can be incompatible with user programs/other libraries that try to bind to the same events.
- Try to be conservative in the number of messages (and especially broadcast messages) you sent per minute. This is to prevent the hardware from overloading. Both esp8266 and esp32 are limited in processing power/memory, making it easy to overload the mesh and destabilise it. And while `painlessMesh` tries to prevent this from happening, it is not always possible to do so.
- Messages can go missing or be dropped due to high traffic and you can not rely on all messages to be delivered. One suggestion to work around is to resend messages every so often. Even if some go missing, most should go through. Another option is to have your nodes send replies when they receive a message. The sending nodes can the resend the message if they haven’t gotten a reply in a certain amount of time.
[more information](https://github.com/gmag11/painlessMesh)
