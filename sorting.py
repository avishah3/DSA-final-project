from nba_api.stats.endpoints import leaguedashplayerstats
import heapq
import time
import random
import string


# Used to create the player list for merge sort
def create_fg_list(n):
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(season='2022-23')
    stats_df = player_stats.get_data_frames()[0]

    if n == 0:
        players_fg_pct = stats_df[['PLAYER_NAME', 'FG_PCT']]
    else:
        players_fg_pct = stats_df[['PLAYER_NAME', 'FG3_PCT']]

    # Convert DataFrame to a list of tuples
    players_fg = list(players_fg_pct.itertuples(index=False, name=None))

    return players_fg


# 100,000 testing requirement
def large_test():
    test_list = list()
    # Generate random strings and numbers
    for i in range(100000):
        random_str = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        random_num = random.random()
        test_list.append([random_str, random_num])
    return test_list


# Times merge sort
def descending(n):
    # unsorted_list = large_test()
    unsorted_list = create_fg_list(n)
    
    start_time = time.time()
    descending_list = merge_sort(unsorted_list)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return [descending_list, elapsed_time]


# Times min heap
def ascending(n):
    # unsorted_list = large_test()
    unsorted_list = create_fg_list(n)
    
    start_time = time.time()
    ascending_list = min_heap(unsorted_list)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return [ascending_list, elapsed_time]


# One of our teammates dropped the class, so we are using STL
def min_heap(arr):
    min_heap = []
    for player in arr:
        heapq.heappush(min_heap, (player[1], player[0]))

    return min_heap


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Recursive call on the left and right halves
        merge_sort(left_half)
        merge_sort(right_half)

        # Merge the sorted halves
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            # Compare based on FG percentage and descending order
            if left_half[i][1] > right_half[j][1]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Check for any remaining elements in the left and right halves
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

    return arr
