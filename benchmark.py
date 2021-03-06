import random

BENCHMARK_FILE_DATAPATH = "./testdata/workload.txt"
LABEL_FILE_PATH = "./testdata/data.txt"


class Benchmark:
    def __init__(self, fpath):
        self.path = fpath
        with open("./testdata/city_population.txt", 'r') as file:
            self.populationlist = [line.rstrip('\n') for line in file]

    def population_get(self):
        return self.populationlist

    def query_read(self):
        with open(self.path, 'r') as f:
            lines = [line.rstrip('\n') for line in f]
        return lines

    def query_write(self, type, table, **kwargs):
        if type == 'read_range':
            """ Generates SQL for a SELECT statement matching the kwargs passed. """
            sql = list()
            sql.append("SELECT city_name, state_name FROM %s " % table)
            if kwargs:
                sql.append("WHERE " + " AND ".join("%s > %d" % (k, v) for k, v in kwargs.items()))
            sql.append(";")
            with open(self.path, 'a') as f:
                f.write("".join(sql) + '\n')
        elif type == 'read_point':
            """ Generates SQL for a SELECT statement matching the kwargs passed. """
            sql = list()
            sql.append("SELECT city_name, state_name FROM %s " % table)
            if kwargs:
                sql.append("WHERE " + " AND ".join("%s = %d" % (k, v) for k, v in kwargs.items()))
            sql.append(";")
            with open(self.path, 'a') as f:
                f.write("".join(sql) + '\n')
        elif type == 'upsert':
            """ update/insert rows into objects table (update if the row already exists)
                    given the key-value pairs in kwargs """
            keys = ["%s" % k for k in kwargs]
            values = ["'%s'" % v for v in kwargs.values()]
            sql = list()
            sql.append("INSERT INTO %s (" % table)
            sql.append(", ".join(keys))
            sql.append(") VALUES (")
            sql.append(", ".join(values))
            sql.append(") ON DUPLICATE KEY UPDATE ")
            sql.append(", ".join("%s = '%s'" % (k, v) for k, v in kwargs.items()))
            sql.append(";")
            with open(self.path, 'a') as f:
                f.write("".join(sql))
        elif type == 'delete':
            """ deletes rows from table where **kwargs match """
            sql = list()
            sql.append("DELETE FROM %s " % table)
            sql.append("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in kwargs.items()))
            sql.append(";")
            with open(self.path, 'a') as f:
                f.write("".join(sql))


if __name__ == '__main__':
    bm = Benchmark(BENCHMARK_FILE_DATAPATH)
    tabname = 'city'
    """
        for i in range(1000):
        num = random.uniform(5.000, 30.000)
        number = num*10000
        bm.query_write('read', tabname, **{"population": number})
    """
    with open(LABEL_FILE_PATH, 'r') as f:
        for line in f:
            i = int(line.rstrip('\n'))
            print(i)
            if i == 1:
                num = random.uniform(5.000, 30.000)
                number = num * 10000
                bm.query_write('read_range', tabname, **{"population": number})
            else:
                num = random.choice(bm.population_get())
                bm.query_write('read_point', tabname, **{"population": int(num)})
