class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []        # Sorted keys
        self.children = []    # Child pointers
        self.values = []      # Values/pointers associated with keys


class BTree:
    def __init__(self, t):
        self.root = BTreeNode()
        self.t = t    # Minimum degree (defines min/max keys per node)

    def search(self, k, node=None):
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        if i < len(node.keys) and k == node.keys[i]:
            return (node, i)
        elif node.leaf:
            return None
        else:
            return self.search(k, node.children[i])

    def insert(self, k, v):
        # First check if key already exists
        if self.search(k) is not None:
            return False  # Key already exists

        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            # Root is full, need to split
            new_root = BTreeNode(leaf=False)
            self.root = new_root
            new_root.children.insert(0, root)
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, k, v)
        else:
            self._insert_non_full(root, k, v)
        return True

    def _split_child(self, parent, i):
        t = self.t
        child = parent.children[i]
        new_child = BTreeNode(leaf=child.leaf)

        # Move key and value to parent
        parent.keys.insert(i, child.keys[t-1])
        parent.values.insert(i, child.values[t-1])
        parent.children.insert(i + 1, new_child)

        # Split keys and values
        new_child.keys = child.keys[t:]
        new_child.values = child.values[t:]
        child.keys = child.keys[:t-1]
        child.values = child.values[:t-1]

        if not child.leaf:
            new_child.children = child.children[t:]
            child.children = child.children[:t]

    def _insert_non_full(self, node, k, v):
        i = len(node.keys) - 1

        if node.leaf:
            # Insert into leaf
            while i >= 0 and k < node.keys[i]:
                i -= 1
            node.keys.insert(i + 1, k)
            node.values.insert(i + 1, v)
        else:
            # Recurse to appropriate child
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1

            if len(node.children[i].keys) == (2 * self.t) - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k, v)


class Record:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender


class Page:
    def __init__(self, size=4096):
        self.size = size
        self.data = []
        self.btree_node = None
        self.page_id = None


class DatabaseEngine:
    def __init__(self):
        self.pages = {}
        self.next_page_id = 0
        self.btree = BTree(2)

    def allocate_page(self):
        page_id = self.next_page_id
        self.next_page_id += 1
        self.pages[page_id] = Page()
        return page_id

    def insert_record(self, record):
        # First store the record in a leaf page
        page_id = self.allocate_page()
        page = self.pages[page_id]
        page.data.append(record)

        # Then insert into B-tree with reference to the page
        return self.btree.insert(record.name, page_id)

    def search(self, name):
        # Find the page containing the record
        result = self.btree.search(name)
        if result is None:
            return None

        node, idx = result
        page_id = node.values[idx]  # Get page ID from values array

        # Load the page and return the record
        page = self.pages[page_id]
        return page.data[0]  # Assuming one record per page for simplicity
