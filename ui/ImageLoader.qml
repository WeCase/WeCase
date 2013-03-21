import QtQuick 1.0

Image {
    id: tweetImage
    source: thumbnail_pic
    
    MouseArea { 
        anchors.fill: parent

        onClicked: {
            busy.on = true;
            console.log("Animation!");
            if (mainWindow.look_orignal_pic(thumbnail_pic)) {
                busy.on = false;
                console.log("No Animation!");
            }
        }
    }

    BusyIndicator {
        id: busy
        scale: 0.5
        anchors.horizontalCenter: parent.horizontalCenter
        on: false
    }
}
