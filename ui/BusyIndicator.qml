import QtQuick 1.0

Image {
    id: container
    property bool on: false
    source: "img/busy.png"; visible: container.on

    NumberAnimation on rotation {
        running: container.on; from: 0; to: 360; loops: Animation.Infinite; duration: 1200
    }
 }
