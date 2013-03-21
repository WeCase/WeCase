import QtQuick 1.0

Image {
    id: tweetImage
    source: thumbnail_pic
    
    MouseArea { 
        anchors.fill: parent

        onClicked: {
            busy.on = true
            mainWindow.look_orignal_pic(thumbnail_pic)
        }
    }

    BusyIndicator {
        id: busy
        scale: 0.5
        anchors.horizontalCenter: parent.horizontalCenter
        on: false
    }
}
