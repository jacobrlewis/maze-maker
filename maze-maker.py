import random
import pygame


class MazeMaker:

    def __init__(self):
        # take inputs to customize
        self.scale = int(input("scale: "))

        self.width = int(input("width: "))
        self.height = int(input("height "))
        self.area = self.height * self.width

        # randomly places the start and end along the top and bottom
        self.start_x = random.randint(0, self.width-1)
        self.end_x = random.randint(0, self.width-1)

        # list of visited squares (x,y)
        self.visited_list = {(self.start_x, 0)}

        # this stack is used for backtracking to fill all squares
        # pieces are stored as [x,y,east connection, south connection]
        self.stack = []
        self.stack.append([self.start_x, 0, False, False])

        # permanently stores all pieces
        self.pieces = [[self.start_x, 0, False, False]]

    def fill(self):
        # run until every place is visited
        while len(self.visited_list) <= self.area - 1:

            # progress bar
            percent = len(self.visited_list)*100/self.area
            print("\r{}% done: |{}{}|".format(percent, "#" * int(percent / 10), "." * (10-int(percent / 9.99))), end="")

            # current piece
            current = self.stack[-1]

            # get direction
            adjacents = self.get_adjacents(current[0], current[1])
            try:
                direction = random.choice(adjacents)
            except IndexError:
                # backtrack if necessary
                self.backtrack()

                continue

            # create next piece and update paths
            if direction == "north":
                #             x         , y             east , south
                next_piece = [current[0], current[1]-1, False, True]

            elif direction == "east":
                next_piece = [current[0]+1, current[1], False, False]
                self.stack[-1][2] = True
                if len(self.pieces) == 1:   # this is needed to update the first piece
                    self.pieces[-1] = self.stack[-1]

            elif direction == "south":
                next_piece = [current[0], current[1]+1, False, False]
                self.stack[-1][3] = True
                if len(self.pieces) == 1:   # this is needed to update the first piece
                    self.pieces[-1] = self.stack[-1]

            elif direction == "west":
                next_piece = [current[0]-1, current[1], True, False]

            # add next square to stack
            self.stack.append(next_piece)

            # add next square to visited list and store it
            self.visited_list.add((next_piece[0], next_piece[1]))
            self.pieces.append(next_piece)

    # returns a list of unvisited adjacents directions
    def get_adjacents(self, x, y):
        adjacents = []

        # above
        if (x, y-1) not in self.visited_list and y != 0:
            adjacents.append("north")
        # right
        if (x+1, y) not in self.visited_list and x != self.width-1:
            adjacents.append("east")
        # below
        if (x, y+1) not in self.visited_list and y != self.height-1:
            adjacents.append("south")
        # left
        if (x-1, y) not in self.visited_list and x != 0:
            adjacents.append("west")

        return adjacents

    # remove from the stack until the last branch is found
    def backtrack(self):
        while True:
            top = self.stack[-1]

            # get adjacents to the point x, y
            adjacents = self.get_adjacents(top[0], top[1])
            if len(adjacents) == 0:
                self.stack.pop()
            else:
                break


def main():
    # this creates the maze
    maze = MazeMaker()
    maze.fill()

    scale = maze.scale

    # pygame stuff
    pygame.init()
    pygame.display.set_caption("Press S to save image")
    print("\nPress S to save image")

    screen = pygame.display.set_mode([maze.width * scale * 2 + scale, maze.height * scale * 2 + scale])

    white = [255, 255, 255]

    running = True
    clock = pygame.time.Clock()

    # draw pieces once
    for piece in maze.pieces:

        # white top left corner of every piece
        pygame.draw.rect(screen, white,
                         pygame.Rect(piece[0] * scale * 2 + scale, piece[1] * scale * 2 + scale, scale, scale))

        # east connection piece
        if piece[2]:
            pygame.draw.rect(screen, white,
                             pygame.Rect(piece[0] * scale * 2 + scale + scale, piece[1] * scale * 2 + scale, scale,
                                         scale))
        # south connection piece
        if piece[3]:
            pygame.draw.rect(screen, white,
                             pygame.Rect(piece[0] * scale * 2 + scale, piece[1] * scale * 2 + scale + scale, scale,
                                         scale))

    # draw start and end squares
    pygame.draw.rect(screen, white, pygame.Rect(maze.start_x * scale * 2 + scale, 0, scale, scale))
    pygame.draw.rect(screen, white,
                     pygame.Rect(maze.end_x * scale * 2 + scale, (maze.height - 1) * scale * 2 + scale + scale, scale,
                                 scale))

    # loop that displays the maze
    while running:
        for event in pygame.event.get():
            # close the window
            if event.type == pygame.QUIT:
                running = False
            # save if 's' is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    filename = input("Enter filename or 'cancel' to cancel. ('.png' is added automatically)\n")
                    if filename != "cancel":
                        pygame.image.save(screen, filename + ".png")
                        print("save successful")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
