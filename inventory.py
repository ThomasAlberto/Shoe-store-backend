# ======PROGRAMME DETAILS======
# This programme simulates a shoe inventory, perhaps the sort that a store manager might use.
# Working with the single class "Shoe", a text file with a bunch of product information, and some empty lists, we build
# a programme that adds new shoes, displays the stock, restocks the lower stocked shoes, displays total value, searches
# by unique product code, and puts the highest stock shoe on sale.


# Tabulate is going to be used later to make the inventory stock look pretty.
from tabulate import tabulate


# ========Class is in Session==========
# The class "Shoe" takes five parameters and initialises them according to user arguments.
# The class has three methods. Funnily enough, I never used these. I wrote a longer function to get the cost and
# quantity of each shoe object to update the lists.
# It also include the "magic method" of __str__ which allow human readability when an individual object is printed.
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"Shoe({self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity})"


# =============Shoe list===========

# We need three empty lists in total. One to store the values taken from the txt file, one to store the objecs, and one
# for that quantity function I mentioned. That will later be used to update the temp list, and from there the txt file.
temp_list = []
shoe_list = []
quantity_list = []


# ==========Functions outside the class==============
# There are seven functions in this section.

# read_shoes_data fills the lists that all the other functions will make use of in some form.
# Inside a try-except clause, this function opens a txt file and appends each line as a sublist of temp_list with each
# element divided by "," using split(), and replaces the "\n" which has been included as an element in each sublist.
# Once this is done it deletes the first line in the new temp_list, which are the headings.
#
# Having done this, the third and fourth indices of each sublist are cast as integers. We need the objects to have cost
# and quantity interpreted as integers for later operations.
#
# Then the elements of the sublists in temp_list are inserted into a for loop which creates a shoe object for every
# sublist in the list.
def read_shoes_data():
    try:
        with open("inventory.txt", "r") as f:
            for line in f:
                line = line.split(",")
                line[-1] = line[-1].replace("\n", "")
                temp_list.append(line[:])
            del temp_list[0]

            for x in range(len(temp_list)):
                temp_list[x][3] = int(temp_list[x][3])
                temp_list[x][4] = int(temp_list[x][4])

            for _item in temp_list:
                shoe_list.append(Shoe(_item[0], _item[1], _item[2], _item[3], _item[4]))

    except FileNotFoundError:
        print("Looks like there was no inventory text file. Check to make sure it's in the path of this Python file.")


# This allows us to create a new shoe obejct and add it to the text file.
# Again, within a try-except clause, we first initialise the object through user input. If the user adds a non-number
# to the cost or quantity variables, it will generate an error, caught by the try-except, and return us to the menu
# without adding a new item. This is important, because otherwise we would have errors in later functions such as
# value_per_item() which does maths operations on all the objects.
#
# Once the input is registered a new Shoe object is made. The object is then appended to shoe_list. From shoe_list,
# temp_list is appended to by calling the attributes of the last element of the recently updated shoe_list in order.
# We could also have gone straight from the new shoe object, but this is fine.
#
# Finally, we overwrite the text file from the temp_list. Remembering to cast each element in each sublist as str,
# because join() only works with strings.
def capture_shoes():

    try:
        inp_country = input("Enter the country the shoe is produced in:\n")
        inp_code = input("Enter the unique identifying product code:\n")
        inp_product = input("Enter the product name:\n")
        inp_cost = int(input("Enter the cost of one pair of these shoes. Do not include a symbol, numbers only:\n"))
        inp_quantity = int(input("Enter the number of shoes in storage. Numbers only:\n"))
        new_shoe = Shoe(inp_country, inp_code, inp_product, inp_cost, inp_quantity)

        shoe_list.append(new_shoe)
        temp_list.append([shoe_list[-1].country, shoe_list[-1].code, shoe_list[-1].product, shoe_list[-1].cost, shoe_list[-1].quantity])

        with open("inventory.txt", "w") as f:
            for sublist in temp_list:
                sublist = list(str(element) for element in sublist)
                f.write(",".join(sublist) + "\n")
        f.close()
    except Exception as error:
        print("We detected an error in one of your inputs. Your new shoe object has not been added to the system. Please try again.")


# This function displays the entire inventory from the shoe_list of objects. For this to work, we require the __str__
# magic method in the class.
# We do this in two ways. First, with a simple for-loop and some text to pretty the display up. Run the loop over every
# object in the shoe_list and print it out. Second, again with the tabulate method which looks really nice.
def view_all():

    print("The following are all the shoes in our inventory\n")
    print("==================================================")
    for shoe in shoe_list:
        print(shoe)
    print("==================================================\n")
    print("And here they are again, tabulated:\n")
    print(tabulate(temp_list, headers=["Country", "Code", "Product", "Cost", "Quantity"], tablefmt="fancy_grid"))
    print("")


# This function identifies the shoe with the smallest total stock and then restocks it according to the quantity
# selected by the user.
# To find the smallest quantity we begin by setting a ceiling to what a quantity can be. I found that Python has defined
# infinity according to their float method. So that's a good place to start. The smallest stock is at most +infinity.
# Define the shoes with the least stock as None for now.
# In a for loop of all the shoes in shoe_list, if the quantity attribute of the shoe object is less than infinity, then
# that is the reassignment to min_quantity (our ceiling) and the min_shoe is the shoe with that attribute.
# Each loop will reassign min_quantity and min_shoe every time it sees a smaller quantity attribute, or it will pass.
#
# At the end we have the minimum shoe and we print out a message saying what it is.
# Having ID'd the min_shoe, we go on to the restock aspect of this function.
# We set up a while loop to get around a typo in the user input.
# The user is asked whether they want to restock the shoe. If "no" then the while loop is broken and user is returned.
# If "yes" then the amount of shoes to restock by is asked of the user. The shoe.quantity attribute is updated by adding
# to it the user input number. Once this is done, the temp_list is updated by using the index of the shoe in the
# shoe_list (temp_list and shoe_list have identical indexes), and the 2d element update of index 4 for the new quantity.
# Once done, and finally, the temp_list is written once again to the txt file.
def re_stock(shoes):

    min_quantity = float('inf')
    min_shoe = None
    for shoe in shoes:
        if shoe.quantity < min_quantity:
            min_quantity = shoe.quantity
            min_shoe = shoe
        else:
            pass

    print(f"The shoe in stock with the smallest quantity is {min_shoe.product} with product code {min_shoe.code}. "
          f"It has {min_shoe.quantity} units currently in stock.")


    break_condition = False
    while not break_condition:
        restock_question = input("Would you like to restock this item? Please enter \'Yes\' or \'No\'.\n")
        if restock_question.lower() == "yes":
            restock_amount = int(input(f"How many new pairs of {min_shoe.product} should we restock?\n"))
            for shoe in shoe_list:
                if min_shoe == shoe:
                    shoe.quantity = shoe.quantity + restock_amount
                    min_shoe_obj_idx = shoe_list.index(shoe)
                    temp_list[min_shoe_obj_idx][4] = shoe.quantity

                    with open("inventory.txt", "w") as f:
                        for sublist in temp_list:
                            sublist = list(str(element) for element in sublist)
                            f.write(",".join(sublist) + "\n")

                    f.close()
                    break_condition = True

                else:
                    pass

        elif restock_question.lower() == "no":
            break_condition = True

        else:
            pass


# This function searches for a shoe object in the shoe_list according to the code attribute.
# First it prompts the user for an ID code.
# Then we enter a While loop. The first part of the While loop iterates over every shoe in the list. If the shoe's
# attribute is equivalent to the id_code, then it prints the shoe. This will only ever print one shoe because the ID
# is unique. The other shoes are passed. Once every shoe has been checked we pass to the next part of the programme.
#
# id_code is reset to some string that isn't any product's unique id code. This has a function which I'll come back to.
# The repeat_condition is prompted, which allows users to search for multiple shoes without restarting the process.
# Entering "yes" prompts an update to the id_code, takes us back to the start of the while loop, and prints any shoe
# with a matching id.
# Entering "no" will break the loop and return the user.
# Entering anything else will print an error message, then return to the beginning of the while loop. But because
# id_code has been updated to "skip", we immediately return to the repeat_condition, effortlessly allowing users to
# circumvent typos.
def search_shoe():

    break_condition = False
    id_code = input("Enter a product ID code to search for it:\n")
    while not break_condition:
        for shoe in shoe_list:
            if shoe.code == id_code:
                print(shoe)
            else:
                pass

        id_code = "skip"
        repeat_condition = input("Would you like to enter another product ID? Enter \'Yes\' or \'No\'.\n")

        if repeat_condition.lower() == "yes":
            id_code = input("Enter a product ID code to search for it:\n")
        elif repeat_condition.lower() == "no":
            break_condition = True
        else:
            print("Sorry, that input wasn't recognised. Please try again.")


# Much simpler function which shows the value (cost * quantity) of each item. For each shoe in the list, the shoe_value
# is assigned the value of the cost attribute multiplied by the quantity attribute.
# It then prints the name of the shoe and the value of the shoe.
def value_per_item():

    for shoe in shoe_list:
        shoe_value = shoe.cost * shoe.quantity
        print(shoe.product)
        print("The value of the entire shoe's stock is: " + "$" + str(shoe_value) + "\n")


# This is something of an inversion of the re_stock() function. Instead of finding the lowest stock, it finds the
# highest stock. Again we define a "floor" for the smallest possible shoe stock, and replace the max_quantity and
# max_shoe each loop depending on whether it finds a shoe object with a higher attribute. There's no need to go back
# over the details as it works in the same way.
# Once the highest product is found, a message that this shoe is on sale is printed.

def highest_qty(shoes):
    max_quantity = 0
    max_shoe = None

    for shoe in shoes:
        if shoe.quantity > max_quantity:
            max_quantity = shoe.quantity
            max_shoe = shoe
        else:
            pass
    print(f"Good news! {max_shoe.product} is for sale!")


# ==========Main Menu=============

# Finally, the main menu is generated.
# This is the simplest part of the programme.
# The read_shoes_data() function is called to fill in the lists.
# A while loop is started.
# Depending on the user's input, each of the six above defined functions are called. The user can also quit
# and break the while loop, ending the programme.

read_shoes_data()
break_condition = False
while not break_condition:
    menu_input = input("""Welcome to the menu. Please enter one of the following options.
    
    Enter \'N\' to enter a new shoe into the shoe inventory.
    Enter \'V\' to view all the shoes in the inventory.
    Enter \'R\' to restock the shoe with the lowest quantity in stock.
    Enter \'S\' to search a shoe in the inventory with its unique product ID.
    Enter \'T\' to display the total value of the stock for every item.
    Enter \'H\' to put the show with the highest stock on sale.
    Enter \'Q\' to quit the programme.
    """)
    if menu_input.lower() == "n":
        capture_shoes()
    elif menu_input.lower() == "v":
        view_all()
    elif menu_input.lower() == "r":
        re_stock(shoe_list)
    elif menu_input.lower() == "s":
        search_shoe()
    elif menu_input.lower() == "t":
        value_per_item()
    elif menu_input.lower() == "h":
        highest_qty(shoe_list)
    elif menu_input.lower() == "q":
        break_condition = True

