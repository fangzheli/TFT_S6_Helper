class TraitRankNode:
    def __init__(self, key, average_place, win_rate, top4_rate, popularity):
        self.left = None
        self.right = None
        self.val = key
        self.average_place = average_place
        self.win_rate = win_rate
        self.top4_rate = top4_rate
        self.popularity = popularity


def insert(root, key, average_place, win_rate, top4_rate, popularity):
    if root is None:
        return TraitRankNode(key, average_place, win_rate, top4_rate, popularity)
    else:
        if root.val == key:
            return root
        elif root.val < key:
            root.right = insert(root.right, key, average_place, win_rate, top4_rate, popularity)
        else:
            root.left = insert(root.left, key, average_place, win_rate, top4_rate, popularity)
    return root


def search(root, key):
    if root is None or root.val == key:
        return root
    if root.val < key:
        return search(root.right, key)
    return search(root.left, key)


def inorder(root):
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)
