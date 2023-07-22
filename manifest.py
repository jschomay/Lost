manifest = [{
    "filename": "bear.jpeg",
    "on_discover": {
        "description":
        "A massive bear stands tall, its powerful presence filling you with both awe and fear. You tread cautiously, knowing any sudden movement could provoke its fierce wrath. Best not to linger. \n(Courage -2)",
        "stats": [{
            "stat": "courage",
            "diff": -2
        }]
    },
    "on_return": {
        "description":
        "The bear is still here, or has it been following you? \n(Courage -4)",
        "stats": [{
            "stat": "courage",
            "diff": -4
        }]
    }
}, {
    "filename": "big trees.jpeg",
    "on_discover": {
        "description":
        "Towering ancient trees surround you, their branches reaching for the heavens. As you walk beneath their majestic canopy, you feel a sense of ancient wisdom and tranquility. \n(Vigor +1)",
        "stats": [{
            "stat": "vigor",
            "diff": 1
        }]
    },
    "on_return": {
        "description":
        "Back at the tall trees, you feel small and alone now. \n(Courage -1)",
        "stats": [{
            "stat": "courage",
            "diff": -1
        }]
    }
}, {
    "filename": "campfire2.png",
    "on_discover": {
        "description":
        "A crackling campfire illuminates the darkness, casting dancing shadows on the surrounding trees. The warmth and flickering glow invite you to sit and gaze up at the starry sky. \n(Vigor +2)",
        "stats": [{
            "stat": "vigor",
            "diff": 2
        }]
    },
    "on_return": {
        "description":
        "The embers have died down somewhat since last here.\n(Vigor +1)",
        "stats": [{
            "stat": "vigor",
            "diff": 1
        }]
    }
}, {
    "filename": "campfire.jpg",
    "on_discover": {
        "description":
        "You approach a campfire, its gentle flames dancing in the night. The comforting glow and the crackling of burning logs are a welcome sight. \n(Vigor +1)",
        "stats": [{
            "stat": "vigor",
            "diff": 1
        }]
    },
    "on_return": {
        "description": "How many campfires are there? \n(Vigor +1)",
        "stats": [{
            "stat": "vigor",
            "diff": 1
        }]
    }
}, {
    "filename": "crows.jpeg",
    "on_discover": {
        "description":
        "The forest grows dark. You hear a fluttering overhead. When you turn, ominous crows stare down at you with beady eyes. Your throat tightens, your mouth goes dry.  \n(Courage -1)",
        "stats": [{
            "stat": "courage",
            "diff": -1
        }]
    },
    "on_return": {
        "description":
        "The crows again!  You are going in circles! \n(Courage -1)",
        "stats": [{
            "stat": "courage",
            "diff": -1
        }]
    }
}, {
    "filename": "foggy path.jpeg",
    "on_discover": {
        "description":
        "A foggy path winds through the dense forest, its misty tendrils concealing secrets and uncertainty. As you tread softly, you sense a hidden presence observing your every move. \n(Courage -1)",
        "stats": [{
            "stat": "courage",
            "diff": -1
        }]
    },
    "on_return": {
        "description": "Are you stil lost in the fog? \n(Courage -2)",
        "stats": [{
            "stat": "courage",
            "diff": -2
        }]
    }
}, {
    "filename": "hills and path.jpg",
    "on_discover": {
        "description":
        "You ascend the hills, the path stretching before you like an adventure waiting to unfold. With each step, excitement fills your chest, and you can't help but wonder what awaits at the summit. \n(Courage +2, Vigor -1)",
        "stats": [{
            "stat": "courage",
            "diff": 2
        }, {
            "stat": "vigor",
            "diff": -1
        }]
    },
    "on_return": {
        "description":
        "A hill climb again?.  Been there, done that. \n(Vigor -1)",
        "stats": [{
            "stat": "vigor",
            "diff": -1
        }]
    }
}, {
    "filename": "hut1.png",
    "on_discover": {
        "description":
        "You made it back home safely!  It's good to be home.  \nYou win!\nPress 'Enter' to play again.",
        "stats": []
    },
    "on_return": {
        "description": "Home sweet home",
        "stats": []
    }
}, {
    "filename": "lamp post.jpg",
    "on_discover": {
        "description":
        "It's getting dark.  You need to find your way back to your cabin.",
        "stats": []
    },
    "on_return": {
        "description": "Oh no. Back where you started. \n(Courage -1)",
        "stats": [{
            "stat": "courage",
            "diff": -1
        }]
    }
}, {
    "filename": "meadow3.jpg",
    "on_discover": {
        "description":
        "You step into a vast, meadow teeming with vibrant wildflowers. The sweet scent of blooming blossoms fills the air, and you find peace in the embrace of nature's untouched beauty.  \n(Courage +2, Vigor +2)",
        "stats": [{
            "stat": "courage",
            "diff": 2
        }, {
            "stat": "vigor",
            "diff": 2
        }]
    },
    "on_return": {
        "description": "The meadow is still beautiful. \n(Vigor +1)",
        "stats": [{
            "stat": "vigor",
            "diff": 1
        }]
    }
}, {
    "filename": "meadow4.jpg",
    "on_discover": {
        "description":
        "A breathtaking meadow stretches before you, a symphony of colors beneath the vast blue sky. As you walk through this enchanting oasis, you feel as though the worries of the world melt away. \n(Vigor +2, Courage +2)",
        "stats": [{
            "stat": "vigor",
            "diff": 2
        }, {
            "stat": "courage",
            "diff": 2
        }]
    },
    "on_return": {
        "description":
        "This is nice, but will you ever find what you were looking for?",
        "stats": []
    }
}, {
    "filename": "path1.jpg",
    "on_discover": {
        "description":
        "A narrow path meanders through the wilderness, leading you to discover hidden landscapes and untold stories. With every twist and turn, anticipation builds.  How long will this journey be?",
        "stats": []
    },
    "on_return": {
        "description": "The long journey goes on and on. \n(Vigor -1)",
        "stats": [{
            "stat": "vigor",
            "diff": -1
        }]
    }
}, {
    "filename": "pond night.jpeg",
    "on_discover": {
        "description":
        "By the tranquil pond, the moon's gentle reflection dances on the rippling water. In the stillness of the night, a sense of serenity envelops you. \n(Courage +1)",
        "stats": [{
            "stat": "courage",
            "diff": 1
        }]
    },
    "on_return": {
        "description": "You've been here already, right?",
        "stats": []
    }
}, {
    "filename": "pond raining.jpeg",
    "on_discover": {
        "description":
        "Raindrops pelt the surface of a desolate pond. The air is heavy with a chill, and the darkness is intensified by the downpour. \n(Courage -1, Vigor -1)",
        "stats": [{
            "stat": "courage",
            "diff": -1
        }, {
            "stat": "vigor",
            "diff": -1
        }]
    },
    "on_return": {
        "description":
        "Still raining, still cold, still wet. \n(Courage -1, Vigor -1)",
        "stats": [{
            "stat": "courage",
            "diff": -1
        }, {
            "stat": "vigor",
            "diff": -1
        }]
    }
}, {
    "filename": "river1.jpg",
    "on_discover": {
        "description":
        "A mighty river rushes past with unrestrained force, blocking your path. You'll have to go around. \n(Vigor -3)",
        "stats": [{
            "stat": "vigor",
            "diff": -3
        }]
    },
    "on_return": {
        "description":
        "You thought you found a way around this.  You were wrong. \n(Vigor -1)",
        "stats": [{
            "stat": "vigor",
            "diff": -1
        }]
    }
}, {
    "filename": "wolves.png",
    "on_discover": {
        "description":
        "You hear howling echoing through the trees. The eerie sound gets closer. This is not good. \n(Courage -3)",
        "stats": [{
            "stat": "courage",
            "diff": -3
        }]
    },
    "on_return": {
        "description": "Why did you come back here? \n(Courage -2)",
        "stats": [{
            "stat": "courage",
            "diff": -1
        }]
    }
}]
