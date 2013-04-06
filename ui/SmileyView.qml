import QtQuick 1.0

Rectangle {
    width: 300; height: 200

    Component {
        id: smileyDelegate
        Item {
            width: grid.cellWidth; height: grid.cellHeight

            Column {
                anchors.fill: parent
                Image { source: portrait; anchors.horizontalCenter: parent.horizontalCenter }
                Text { text: name; anchors.horizontalCenter: parent.horizontalCenter }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        highlight: color: "lightsteelblue"; radius: 5 
                        grid.currentIndex = index 
                    }
                }
            }
        }
    }

    GridView {
        id: grid
        anchors.fill: parent
        cellWidth: 30; cellHeight: 30

        model: SmileyModel {}
        delegate: smileyDelegate
        highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
        focus: true
    }
}
