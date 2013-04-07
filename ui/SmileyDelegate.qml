import QtQuick 1.0


Item {
    width: grid.cellWidth; height: grid.cellHeight

    Column {
        anchors.fill: parent
        Image { source: path; anchors.horizontalCenter: parent.horizontalCenter }
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
