"""
布隆过滤
"""

class BloomFilter(object):
    
    def __init__(self, size):
        """
        Initialization BF size
        """
        self.values = [False] * size
        self.size = size

    def hash_value(self, value):
        """
        Hash the value
        """
        return hash(value) % self.size

    def add_value(self, value):
        """
        Add a value to the BF
        """
        h = self.hash_value(value)
        self.values[h] = True

    def might_contain(self, value):
        """
        Check if the value might be in the BF
        """
        h = self.hash_value(value)
        return self.values[h]

    def print_contents(self):
        print(self.values)


bf = BloomFilter(10)
bf.add_value('dog')
bf.add_value('cat')
bf.add_value('fish')
bf.print_contents()
bf.add_value('bird')
bf.print_contents()
for term in ['dog', 'fish', 'cat', 'bird', 'duck', 'emu']:
    print('{}: {} {}'.format(term, bf.hash_value(term), bf.might_contain(term)))

"""
OUT1:
[True, False, False, False, False, False, True, False, False, False]
[True, False, False, False, False, False, True, False, False, False]
dog: 6 True
fish: 0 True
cat: 6 True
bird: 0 True
duck: 7 False
emu: 3 False

OUT2:
[False, True, False, False, True, False, False, False, False, True]
[False, True, False, True, True, False, False, False, False, True]
dog: 1 True
fish: 4 True
cat: 9 True
bird: 3 True
duck: 6 False
emu: 6 False
"""

def major_segments(s):
    major_breaks = ' '
    last = -1
    results = set()

    # enumerate() will give us (0, s[0]) (1, s[1]) ...
    for idx, ch in enumerate(s):
        if ch in major_breaks:
            segment = s[last+1:idx]
            results.add(segment)
            last = idx
    segment = s[last+1:]
    results.add(segment)
    return results

def minor_segments(s):
    minor_breaks = '_.'
    last = -1
    results = set()
    for idx, ch in enumerate(s):
        if ch in minor_breaks:
            segment = s[last+1:idx]
            results.add(segment)
            segment = s[:idx]
            results.add(segment)
            last = idx
    segment = s[last+1:]
    results.add(segment)
    results.add(s)
    return results

def segments(event):
    results = set()
    for major in major_segments(event):
        for minor in minor_segments(major):
            results.add(minor)
    return results


class Splunk(object):
    def __init__(self):
        self.bf = BloomFilter(64)
        self.terms = {}
        self.events = []
    
    def add_event(self, event):
        event_id = len(self.events)
        self.events.append(event)
        for term in segments(event):
            self.bf.add_value(term)
            if term not in self.terms:
                self.terms[term] = set()
            self.terms[term].add(event_id)
    def search(self, term):
        if not self.bf.might_contain(term):
            return
        if term not in self.terms:
            return
        for event_id in sorted(self.terms[term]):
            yield self.events[event_id]


def main():
    for term in segments('src_ip = 1.2.3.4'):
        print(term)
    
    s = Splunk()
    s.add_event('src_ip = 1.2.3.4')
    s.add_event('src_ip = 5.6.7.8')
    s.add_event('dst_ip = 1.2.3.4')

    print('============================')
    for event in s.search('1.2.3.4'):
        print(event)
    print('====================')
    for event in s.search('src_ip'):
        print(event)
    print('========================')
    for event in s.search('ip'):
        print(event)

if __name__ == '__main__':
    main()