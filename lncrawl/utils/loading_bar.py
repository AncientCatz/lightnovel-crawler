# -*- coding: utf-8 -*-

def progress(count, total, status=''):
    bar_len = 10
    filled_len = int(bar_len * count / float(total))

    percents = round(100.0 * count / float(total), 1)
    bar = '●' * filled_len + '○' * (bar_len - filled_len)

    loading = ('[%s] %s%s · %s/%s\n%s\r' % (bar, percents, '%', count, total, status))
    return loading
    # sys.stdout.write('[%s] %s%s · %s / %s ·%s\r' % (bar, percents, '%', count, total, status))
    # sys.stdout.flush()


# Usage
# total = 1000
# i = 0
# while i < total:
#     print(progress(i, total, status='Loading'))
#     time.sleep(0.5)  # emulating long-playing job
#     i += 1