import QtQuick 1.0

Rectangle {
    id: container
    width: 283
    height: 504

    color: "#ffffff"

    function positionViewAtBeginning() { 
        tweetListView.positionViewAtBeginning();
    }

    function imageLoaded(tweetid) {
        var item = getDelegateInstanceAt(tweetid)
        item.imageLoaded()
    }

    function getDelegateInstanceAt(tweetid) {
        for (var i = 0; i < tweetListView.contentItem.children.length; i++) {
            var item = tweetListView.contentItem.children[i];
            if (item.tweetid == tweetid) {
                return item;
            }
        }
        return undefined;
    }

    ListView {
        id: tweetListView
        anchors.fill: parent;
        clip: true
        model: mymodel
        delegate: TweetDelegate {

            function retweet_string() {
                if (tweetType == "retweet") {
                    return "//@" + tweetScreenName + ":" + tweetText;
                }
                else {
                    return "";
                }
            }

            function favorite() {
                if (isFavorite) {
                    if (mainWindow.un_favorite(tweetid)) {
                        isFavorite = false;
                    }
                }
                else {
                    if (mainWindow.favorite(tweetid)) {
                        isFavorite = true;
                    }
                }
            }

            tweetType: type
            tweetScreenName: author
            tweetOriginalId: original_id
            tweetOriginalName: original_author
            tweetOriginalText: original_content
            tweetText: content
            tweetAvatar: avatar
            tweetid:  id
            isOwnTweet: true
            isNewTweet: true
            isFavorite: false
            tweetSinceTime: time

            onFavoriteButtonClicked: favorite()
            onRetweetButtonClicked: mainWindow.repost(tweetid, retweet_string())
            onCommentButtonClicked: mainWindow.comment(tweetid)
            onReplyButtonClicked: mainWindow.reply(original_id, tweetid)

            // not implemented
            onMoreButtonClicked: console.log("Clicked a user: " + tweetScreenName)
            onHashtagLinkClicked: console.log("Clicked a tag: " + hashtag)
            onMentionLinkClicked: console.log("Clicked a mention: " + screenname)
        }

        onMovementEnded: {
            // load more tweets
            if (atYEnd) {
                mainWindow.load_more()
            }
        }
    }

    Rectangle {
        id: scrollbar
        anchors.right: tweetListView.right
        y: tweetListView.visibleArea.yPosition * tweetListView.height
        width: 2
        height: tweetListView.visibleArea.heightRatio * tweetListView.height
        color: "black"
    }
}
