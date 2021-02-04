import sys
import os

class Theater:

    def __init__(self, num_rows=10, num_cols=20):
        # theater size given in the specs
        self.num_rows = num_rows
        self.num_cols = num_cols
        # 0 represents vacant seating, 1 represents taken seating, 2 represents already buffered seats, 3 represents
        # the buffer zone about to be created
        self.seating = [[0 for _ in range(num_cols)] for _ in range(num_rows)]
        self.available_seats = num_rows * num_cols
        self.reservations = []
        self.bottom_right = (num_rows-1, num_cols-1)
        self.buffer_space = [(0,-1,), (0,-2,), (0,-3,), (0,1,), (0,2,), (0,3,), (-1,0,), (-1,-1,), (-1,-2,), (-1,-3,),
                             (-1,1,), (-1,2,), (-1,3,)]

    # returns the number of seats to reserve, and then -1 on failure to parse a line of input
    def parse_reservation(self, reservation):
        # correct reservation format is R### #
        reservation_components = reservation.split(" ")
        if len(reservation_components) != 2:
            print("reservation format: R### #")
            return -1
        reservation_id = reservation_components[0]
        number_seats = reservation_components[1]

        if len(reservation_id) != 4 or reservation_id[0] != "R" or not reservation_id[1:].isnumeric() or \
                not number_seats.isnumeric():
            print("reservation format: R### #")
            return -1
        if int(number_seats) > 0:
            self.reservations.append([reservation_id, int(number_seats), []])

    # if we reach the end of a row and need more seats, then decrement row counter by 1, otherwise if we reach a buffer
    # and need more seats, go to the beginning of the current row and decrement the row by 1
    def fill_seats(self):
        for reservation in self.reservations:
            right_to_left = True
            number_seats = reservation[1]
            if self.bottom_right == (-1, -1) or number_seats > self.available_seats:
                reservation[2] = "Theater is full, please try again next time."
                continue
            curr_row, curr_col = self.bottom_right
            while number_seats:
                # move up one row from the right side, continue going right-to-left
                if curr_col > self.num_cols-1:
                    right_to_left = True
                    curr_row -= 1
                    curr_col = self.num_cols-1
                # move up one row from the left side, now need to move left-to-right
                elif curr_col < 0:
                    right_to_left = False
                    curr_row -= 1
                    curr_col = 0
                else:
                    # check if we ran into a buffer zone
                    if self.seating[curr_row][curr_col] == 2:
                        if right_to_left:
                            curr_col = self.num_cols + 1
                        else:
                            curr_col = -2
                    # otherwise we are checking if we can assign the current square
                    else:
                        if self.seating[curr_row][curr_col] == 0 or self.seating[curr_row][curr_col] == 3:
                            number_seats -= 1
                            if self.seating[curr_row][curr_col] == 0:
                                self.available_seats -= 1
                            self.seating[curr_row][curr_col] = 1
                            self.create_buffer(curr_row, curr_col)
                            reservation[2].append((curr_row, curr_col,))
                    if right_to_left:
                        curr_col -= 1
                    else:
                        curr_col += 1
            self.finalize_buffer()
            self.find_bottom_right()

    def find_bottom_right(self):
        for row_ind in range(self.num_rows - 1, -1, -1):
            for col_ind in range(self.num_cols - 1, -1, -1):
                if self.seating[row_ind][col_ind] == 0:
                    self.bottom_right = (row_ind, col_ind)
                    return
        self.bottom_right = (-1, -1)

    def finalize_buffer(self):
        for row_ind in range(self.num_rows - 1, -1, -1):
            for col_ind in range(self.num_cols - 1, -1, -1):
                if self.seating[row_ind][col_ind] == 3:
                    self.seating[row_ind][col_ind] = 2

    def create_buffer(self, curr_row, curr_col):
        for buff_row, buff_col in self.buffer_space:
            if 0 <= curr_row+buff_row < self.num_rows and 0 <= curr_col+buff_col < self.num_cols \
                    and self.seating[curr_row+buff_row][curr_col+buff_col] == 0:
                self.seating[curr_row + buff_row][curr_col + buff_col] = 3
                self.available_seats -= 1

    def write_seats(self, write_f):
        row_to_letter = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J'}
        for reservation in self.reservations:
            if isinstance(reservation[2], str):
                write_f.write(f"{reservation[0]}: {reservation[2]} \n")
            else:
                for ind in range(len(reservation[2])):
                    row_val, col_val = reservation[2][ind]
                    reservation[2][ind] = row_to_letter[row_val]+str(col_val+1)
                output_list = ",".join(reservation[2])
                write_f.write(f"{reservation[0]}: {output_list} \n")

# takes the complete path to a file and outputs to another file, whose path is outputed to the terminal
def main():
    theater = Theater()
    cur_path = os.path.dirname(os.path.realpath(__file__))
    if len(sys.argv) != 2:
        print("command format: python main.py [input]")
        return -1
    f = sys.argv[1]

    try:
        f = open(f, 'r')
        cur_path += "\\theater_seating_output.txt"
        f_write = open(cur_path, 'w')
    except:
        print("file could not be found")
        return -2
    f_line = f.readline()
    while f_line:
        f_line = f_line.strip()
        if f_line:
            if theater.parse_reservation(f_line) == -1:
                return -1
        f_line = f.readline()
    theater.fill_seats()
    theater.write_seats(f_write)
    print(f"Output file path is: {cur_path}")

    f.close()
    f_write.close()


if __name__ == '__main__':
    main()
