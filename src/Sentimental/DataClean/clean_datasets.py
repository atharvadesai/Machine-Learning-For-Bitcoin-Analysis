from clean_abc import clean_abcnews_data
from clean_cnbc import clean_cnbc_data
from clean_guardian import clean_guardian_data
from clean_reuters import clean_reuters_data
from clean_reddit import clean_reddit_data
def clean_data_sets():
    clean_abcnews_data()
    from multiprocessing import Pool, cpu_count
    pool = Pool(max(cpu_count(), 4))
    results = []
    for func in [clean_cnbc_data,
        clean_guardian_data,
        clean_reddit_data,
        clean_reuters_data]:
        results.append(pool.apply_async(func))
    pool.close()
    pool.join()
    [x.get() for x in results]
if __name__ == '__main__':
    clean_data_sets()





