import gzip
import csv

PATH = "/home/ec2-user/us_cameras/"
FILE_NAME = "{}amazon_reviews_us_Camera_v1_00.tsv.gz".format(PATH)


def split_file():
    with gzip.open(filename=FILE_NAME, mode="rt") as g:
        reader = csv.reader(g, delimiter="\t")
        header = next(reader)
        print(header)
        row_list = list()
        row_list.append(header)
        file_count = 0
        for line in reader:
            row_list.append(line)
            if file_count == 20:
                break
            if len(row_list) >= 20000:
                write_new_file(row_list, file_count)
                file_count += 1
                row_list = list()
                row_list.append(header)


def write_new_file(lines, file_count):
    file_name = "{p}amazon_reviews_us_Camera_v1_00_pt{fc}.tsv.gz".format(p=PATH, fc=file_count)
    with gzip.open(filename=file_name, mode="wt") as w:
        writer = csv.writer(w, delimiter="\t")
        for line in lines:
            writer.writerow(line)


if __name__ == "__main__":
    split_file()
