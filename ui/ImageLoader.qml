import QtQuick 1.0

Image {
    id: tweetImage
    source: thumbnail_pic
    
    MouseArea { 
        anchors.fill: parent

        // not implemented
        onClicked: console.log("Clicked a image: " + thumbnail_pic);
    }
}
