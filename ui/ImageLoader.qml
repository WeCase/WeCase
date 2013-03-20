import QtQuick 1.0

Image {
    id: tweetImage
    source: thumbnail_pic
    
    MouseArea { 
        anchors.fill: parent

        // not implemented
        onClicked: mainWindow.look_orignal_pic(thumbnail_pic)
    }
}
