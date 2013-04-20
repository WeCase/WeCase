import QtQuick 1.0

Item  {
    id: container

    property string tweetid
    property string tweetType
    property string tweetScreenName: "Screen Name"
    property string tweetOriginalId
    property string tweetOriginalName: ""
    property string tweetOriginalText: ""
    property string tweetText: "Lorem ipsum dolor sit amet consectetur adipiscing elit. Etiam ac venenatis ante. Ut euismod tempor erat, eget tincidunt elit ultricies sed."
    property string tweetAvatar
    property string tweetSinceTime: "sometimes ago"
    property bool isOwnTweet: true
    property bool isNewTweet: false
    property bool isFavorite: false

    signal retweetButtonClicked
    signal favoriteButtonClicked
    signal commentButtonClicked
    signal replyButtonClicked

    // not implemented
    signal moreButtonClicked
    signal hashtagLinkClicked(string hashtag)
    signal mentionLinkClicked(string screenname)

    width: ListView.view.width;
    height: {
        var tweetImageHeight = tweetImage.paintedHeight
        if (statusText.paintedHeight < 80) {
            return 90 + tweetImageHeight;
        }
        else {
            return statusText.paintedHeight + tweetImageHeight + 20;
        }
    }

    function handleLink(link) {
        if (link.slice(0, 3) == 'tag') {
            hashtagLinkClicked(link.slice(6))
        } else if (link.slice(0, 4) == 'http') {
            Qt.openUrlExternally(link);
        } else if (link.slice(0, 7) == 'mention') {
            mentionLinkClicked(link.slice(10));
        }
    }

    function addTags(str) {
        // surrounds http links with html link tags
        var ret1 = str.replace(/@[-a-zA-Z0-9_\u4e00-\u9fa5]+/g, '<a href="mention://$&">$&</a>');
        var ret2 = ret1.replace(/(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig, "<a href='$1'>$1</a>");
        var ret3 = ret2.replace(/[#]+[&-a-zA-Z0-9_\u4e00-\u9fa5]+[#]/g, '<a href="tag://$&">$&</a>')
        return ret3;
    }

    function imageLoaded() {
        busy.on = false;
    }

    Image {
        id: background
        anchors.fill: parent
        source: {
            if (isOwnTweet)
                return "img/blue_gradient.png"
            else if (isNewTweet)
                return "img/yellow_gradient.png"
            else
                return "img/gray_gradient.png"
        }
    }

    function get_thumbnail_pic() {
        if (thumbnail_pic) {
            console.log(thumbnail_pic)
            return thumbnail_pic
        }
        if (original && original.thumbnail_pic) {
            console.log(original.thumbnail_pic)
            return original.thumbnail_pic
        }
        else {
            return ""
        }
    }


    Rectangle {
        id: avatarBackground
        width: 60
        height: 60
        color: "#00000000"
        border.width: 4
        anchors.top: parent.top
        anchors.topMargin: 10
        anchors.left: parent.left
        anchors.leftMargin: 10
        border.color: "#2bace2"

        Image {
            id: avatarImage
            width: 56
            height: 56
            anchors.centerIn: parent
            smooth: true
            fillMode: Image.Stretch
            source: tweetAvatar

            MouseArea {
                id: avatarImageMouseArea
                anchors.fill: parent

                onClicked: moreButtonClicked()
            }
        }
    }

    ButtonImage {
        id: comment
        visible: tweetType != 2;

        buttonImageUrl: "img/small_comment_button.png"
        pressedButtonImageUrl: "img/small_comment_button_pressed.png"

        width: 15; height: 15
        anchors.top: parent.top; anchors.topMargin: 10
        anchors.right: parent.right; anchors.rightMargin: 10

        onClicked: commentButtonClicked()
    }

    ButtonImage {
        id: retweet
        visible: tweetType != 2;

        buttonImageUrl: "img/small_retweet_button.png"
        pressedButtonImageUrl: "img/small_retweet_button_pressed.png"

        width: 16; height: 16
        anchors.top: comment.bottom
        anchors.topMargin: 17
        anchors.right: parent.right
        anchors.rightMargin: 7

        onClicked: retweetButtonClicked();
    }

    ButtonImage {
        id: reply
        visible: tweetType == 2;

        buttonImageUrl: "img/small_reply_button.png"
        pressedButtonImageUrl: "img/small_reply_button_pressed.png"

        width: 15; height: 8
        anchors.top: parent.top; anchors.topMargin: 10
        anchors.right: parent.right; anchors.rightMargin: 10

        onClicked: replyButtonClicked();
    }

    ButtonImage {
        id: favorite
        visible: tweetType != 2;

        buttonImageUrl: {
            if (isFavorite) {
                return "img/small_favorite_button_pressed.png"
            }
            else {
                return "img/small_favorite_button.png"
            }
        }

        pressedButtonImageUrl: {
            if (isFavorite) {
                return "img/small_favorite_button.png"
            }
            else {
                return "img/small_favorite_button_pressed.png"
            }
        }

        width: 16; height: 16
        anchors.top: retweet.bottom
        anchors.topMargin: 16
        anchors.right: parent.right
        anchors.rightMargin: 7

        onClicked: favoriteButtonClicked();
    }

    Text {
        id: statusText
        color: "#333333"
        text: {
            if (tweetType == 0 || tweetType == 2) {
                return '<b>' + tweetScreenName + ':<\/b><br \/> ' + addTags(tweetText)
            }
            else if (tweetType == 1) {
                return '<b>' + tweetScreenName + ':<\/b><br \/> ' + addTags(tweetText) +
                '<br \/> <b>' + '&nbsp;&nbsp;&nbsp;&nbsp;' + tweetOriginalName + '<\/b>: '
                + addTags(tweetOriginalText)
            }
        }
        anchors.topMargin: 4
        anchors.top: parent.top;
        anchors.right: retweet.left; anchors.rightMargin: 0
        anchors.left: avatarBackground.right; anchors.leftMargin: 10
        textFormat: Text.RichText
        wrapMode: "Wrap"
        font.family: "Segoe UI"
        font.pointSize: 9

        onLinkActivated: container.handleLink(link);
    }

    Image {
        id: tweetImage
        visible: get_thumbnail_pic()
        anchors.top: statusText.bottom
        anchors.topMargin: get_thumbnail_pic() ? 10 : 0;
        anchors.horizontalCenter: parent.horizontalCenter
        source: get_thumbnail_pic()

        MouseArea { 
            anchors.fill: parent

            onClicked: {
                busy.on = true;
                mainWindow.look_orignal_pic(get_thumbnail_pic(), tweetid);
            }
        }

        BusyIndicator {
            id: busy
            scale: 0.5
            anchors.horizontalCenter: parent.horizontalCenter
            on: false
        }
    }

    Text {
        id: sinceText
        text: tweetSinceTime
        anchors.top: avatarBackground.bottom
        anchors.leftMargin: 11
        anchors.topMargin: 5
        anchors.left: parent.left
        font.family: "Segoe UI"
        font.pointSize: 7
    }
}
