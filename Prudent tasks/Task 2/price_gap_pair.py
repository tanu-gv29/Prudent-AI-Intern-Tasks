def find_price_gap_pair(nums, k):
    seen = {}
    best_pair = None
    for j, num in enumerate(nums):
        for target in (num - k, num + k):
            if target in seen:
                i = seen[target]
                if i < j:
                    pair = (i, j)
                    if best_pair is None or pair < best_pair:
                        best_pair = pair
        if num not in seen:
            seen[num] = j
    return best_pair

# nums = list(map(int, input("Enter numbers separated by space: ").split()))
# k = int(input("Enter k value: "))
# print(find_price_gap_pair(nums, k))
