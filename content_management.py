from posts import blogExample

script, example = blogExample()


def Content():
    TOPIC_DICT = {"Blog":[["Introduction","/introduction/", "Our first program", script[0][0], example[0][0]],\
                ["K Neighbours Classifier in Scikit Learn", "/second-post/", "A simple script using K Neighbours Classifier to predict iris species", script[1][0], example[1][0]],\
                ]}
    return TOPIC_DICT
