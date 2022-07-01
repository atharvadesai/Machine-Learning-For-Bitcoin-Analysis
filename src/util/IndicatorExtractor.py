"""
    The part of this file that is useful for entities outside of this file is the ExtractIndicatorData function.
    It runs an instance of Backtrader's Cerebro and iterates over the indicators and writes their values to a
    .csv file.
    If you have any questions, let me know
    - Ben
"""
import backtrader as bt

class IndicatorIterator(bt.Strategy):
    # Indicator names is a string of names separated by commas, if none will be set to I0, I1, ...
    params = (('indicators', []), ('filename', 'DataClean.csv'), ('column_names', None), ('writer_queue', None))

    def __init__(self):
        self.filename = self.p.filename
        self.indicators = self.p.indicators()()
        self.q = self.p.writer_queue

        if self.p.column_names is None:
            names = []

            for i in range(len(self.indicators)):
                for l in range(len(self.indicators[i].lines.lines)):
                    names.append("I{0}L{1}".format(i, l))
            column_names = ",".join(names)
        else:
            column_names = self.p.column_names

        f = open(self.filename, "w")
        f.write(column_names + "\n")
        f.close()

    def next(self):

        if True in [True in [
            len(y) == 0 for y in x.lines.lines
        ]
                    for x in self.indicators]:
            # Skip the first couple of bars so the indicators can start generating meaningful data
            return
        values = []
        for i in range(len(self.indicators)):
            for l in range(len(self.indicators[i].lines.lines)):
                new_value = self.indicators[i].lines.lines[l][0]
                values.append(new_value)
        string = ",".join([str(x) for x in values]) + "\n"
        self.q.append(string)


def ExtractIndicatorData(data_feed, indicator_initializers, filename, column_names=None):
    """
    :param data_feed: Backtrader Datafeed
    :param indicator_initializers: function that returns a function that initializes the indicators
                        It needs to be a function that returns a function so that 'self' can be used inside
                    the IndicatorIterator's init function. Also, you can preset any additional arguments for the
                    indicators when you pass it in.
    :param filename: The file to write the data to
    :param column_names: The names for each column in the table. Defaults to I0L0, I0L1, ..., I1L0, I1L1, ...
    """
    q = []
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(10000)
    cerebro.adddata(data_feed)

    cerebro.addstrategy(IndicatorIterator, indicators=indicator_initializers,
                        filename=filename, column_names=column_names, writer_queue=q)
    cerebro.run()
    f = open(filename, "a")
    f.write("".join(q))
    f.close()
    del cerebro, q
