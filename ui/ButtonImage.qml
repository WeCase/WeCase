import QtQuick 1.0

Item {
    id: btnImage

    property string buttonImageUrl
    property string pressedButtonImageUrl

    signal clicked

    Image {
        id: buttonImage
        source: buttonImageUrl
        anchors.fill: parent
    }

    MouseArea {
        id: mouseRegion
        anchors.fill: parent

        onClicked: btnImage.clicked();
    }

    states: [
        State {
            name: "pressed"
            when: mouseRegion.pressed
            PropertyChanges { target: buttonImage; source: pressedButtonImageUrl }
        }
    ]
}
