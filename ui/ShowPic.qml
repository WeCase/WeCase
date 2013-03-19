import Qt 4.7

Rectangle {
        id: picWindow
        property int max_width: 800
        property int max_height: 600
        property string pic_url:"pic/MainWindow.png"
        width: 320
        height: 240
        color: "black"
        Image {
                id: show_image
                source: pic_url
                smooth: true
                fillMode: Image.PreserveAspectFit
                MouseArea {
                        anchors.fill: parent
                        drag.target: show_image
                        drag.maximumX: 0
                        drag.minimumX: picWindow.width - show_image.width
                        drag.maximumY: 0
                        drag.minimumY: picWindow.height - show_image.height
                }
        }
}
