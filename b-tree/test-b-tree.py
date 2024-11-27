from btree import BTree, DatabaseEngine, Record


def visualize_tree(node, level=0, prefix="Root: "):
    """Print a visual representation of the tree with both keys and values"""
    key_val_pairs = [f"{k}:{v}" for k, v in zip(node.keys, node.values)]
    print("  " * level + prefix + str(key_val_pairs))
    if not node.leaf:
        for i, child in enumerate(node.children):
            visualize_tree(child, level + 1, f"Child {i}: ")


def test_btree_visualization():
    # Create a B-tree with minimum degree 2
    btree = BTree(2)

    print("\nInserting numbers 1-7 with values being double the key:")
    for i in range(1, 8):
        btree.insert(i, i*2)  # key is i, value is i*2
        print(f"\nAfter inserting {i}:")
        visualize_tree(btree.root)
        print("-" * 40)


def test_random_insertions():
    import random

    btree = BTree(2)
    numbers = list(range(1, 11))
    random.shuffle(numbers)

    print("\nInserting 10 random numbers:")
    print(f"Insertion order: {numbers}")

    for num in numbers:
        btree.insert(num, num*100)  # key is num, value is num*100
        print(f"\nAfter inserting {num}:")
        visualize_tree(btree.root)
        print("-" * 40)


def test_duplicate_prevention():
    print("\n=== Testing duplicate prevention ===")
    btree = BTree(2)

    # Try inserting same key with different values
    print("\nTrying to insert key 5 three times with different values:")
    print("First insertion:", btree.insert(5, 500))
    print("Second insertion:", btree.insert(5, 501))
    print("Third insertion:", btree.insert(5, 502))

    print("\nTree after attempting duplicate insertions:")
    visualize_tree(btree.root)

    # Try more complex scenario
    entries = [(3, 300), (3, 301), (7, 700), (7, 701)]
    print(f"\nTrying to insert sequence with duplicates:")
    for key, value in entries:
        success = btree.insert(key, value)
        print(
            f"Inserting key {key} with value {value}: {'Success' if success else 'Failed - duplicate key'}")

    print("\nFinal tree:")
    visualize_tree(btree.root)


def test_database():
    print("\n=== Testing database operations ===")
    db = DatabaseEngine()

    # Insert records
    records = [
        Record("Alice", 27, 0),
        Record("Bob", 32, 1),
        Record("Cecil", 35, 0)
    ]

    print("\nInserting records:")
    for record in records:
        success = db.insert_record(record)
        print(f"Inserted {record.name}: {'Success' if success else 'Failed'}")
        print("\nB-tree state:")
        visualize_tree(db.btree.root)
        print("-" * 40)

    # Test searches
    print("\nTesting searches:")
    for name in ["Alice", "Bob", "Cecil", "David"]:
        record = db.search(name)
        if record:
            print(f"Found {name}: Age={record.age}, Gender={record.gender}")
        else:
            print(f"{name} not found")


if __name__ == "__main__":
    print("=== Testing basic key-value insertions ===")
    test_btree_visualization()

    print("\n=== Testing random key-value insertions ===")
    test_random_insertions()

    print("\n=== Testing duplicate prevention ===")
    test_duplicate_prevention()

    print("\n=== Testing database operations ===")
    test_database()
