import mainsequential as seq
import mainpool as pl
import statistics


def main():
    seq_list = []
    for i in range(10):
        seq_list.append(seq.main())

    pool_list = []
    for i in range(10):
        pool_list.append(pl.main())

    print('*' * 80)
    print('SEQUENTIAL')
    print(seq_list)

    print('POOL:')
    print(pool_list)

    print('SEQ avg:' + str(statistics.mean(seq_list)))
    print('POOL avg:' + str(statistics.mean(pool_list)))

    print('*' * 80)


if __name__ == '__main__':
    main()
