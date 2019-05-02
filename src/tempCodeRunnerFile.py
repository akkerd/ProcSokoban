
for row in level.values():
    if "a" in row:
        row[row.index("a")] = "0"
        break


print("Final Iteration: ")
print_and_write_grid(level, "Test")