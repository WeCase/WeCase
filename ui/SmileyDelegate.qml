import QtQuick 1.0

Item {
    width: grid.cellWidth; height: grid.cellHeight

    Item {
        anchors.fill: parent

        Image { 
            id: smileyImg; 
            source: path; 
            anchors.horizontalCenter: parent.horizontalCenter 
        }

        Text {
            id: smileyName;
            text: name; 
            anchors.top: smileyImg.top;
            anchors.topMargin: 22
            anchors.horizontalCenter: parent.horizontalCenter
        }

        MouseArea {
            anchors.fill: parent

            onClicked: {
                highlight: color: "lightsteelblue"; radius: 5 
                grid.currentIndex = index 
            }

            onDoubleClicked: {
                parentWindow.returnSmileyName('[' + name + ']')
            }
        }
    }
}
