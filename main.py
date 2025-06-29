import mysql.connector

con = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "An1t@040808",
    database = "books"
)

mysql = con.cursor()
mysql.execute("SELECT * FROM reading_log")
mysql.fetchall()

while True:
    choice = int(input("\n1.New Entry\n2.Delete Entry\n3.Wishlist\n4.Browse Entries\n5.View Stats\n6.Exit\n"))
    # title, author, genre, status, rating, notes

    if choice == 1:
        print("----New Entry----")
        title = input("Book Title: ") or None
        author = input("Author: ") or None
        genre = input("Genre: ") or None
        status = input("Reading Status: ") or None
        rating_in = input("Book Rating: ")
        rating = float(rating_in) if rating_in else None
        notes = input("Additional Notes: ") or None

        insert = "INSERT INTO reading_log (title,author,genre,status,rating,notes) VALUES (%s,%s,%s,%s,%s,%s)"
        vals = (title,author,genre,status,rating,notes)
        mysql.execute(insert,vals)
        con.commit()
        print("New Entry Added!")

    elif choice == 2:
        print("----Delete Entry----")
        book_title = input("Book Title: ")
        select = 'SELECT title,author FROM reading_log WHERE title = %s'
        mysql.execute(select,(book_title,))
        query = mysql.fetchall()
        print(query)
        confirm = input("Are you sure? [y/n] ")

        if confirm == "n" or confirm == "N":
            continue

        elif confirm == "y" or confirm == "Y":
            delete = "DELETE FROM reading_log WHERE title = %s"
            mysql.execute(delete,(book_title,))
            con.commit()
            print("Entry Deleted!")

        else:
            continue

    elif choice == 3:
        print("----Wishlist----")
        wish = "SELECT * FROM reading_log WHERE status = %s"
        w_list = "Wishlist"
        mysql.execute(wish,(w_list,))
        wishlist = mysql.fetchall()
        print(wishlist)

    elif choice == 4:
        print("----All Entries----")
        mysql.execute("SELECT * FROM reading_log")
        all = mysql.fetchall()
        for row in all:
            print(row)

    elif choice == 5:
        # total books, books completed, avg rating, most read genre
        mysql.execute("SELECT COUNT(*) FROM reading_log")
        total = mysql.fetchall()
        print("Total Books Read: ", total)

        complete = "SELECT COUNT(id) FROM reading_log WHERE status = %s"
        c = "Completed"
        mysql.execute(complete,(c,))
        completed = mysql.fetchall()
        print("Books Completed: ",completed)

        mysql.execute("SELECT AVG(rating) FROM reading_log WHERE rating IS NOT NULL")
        rating = mysql.fetchall()
        print("Average Rating: ",rating)

        mysql.execute("SELECT genre FROM reading_log GROUP BY genre ORDER BY COUNT(genre) DESC LIMIT 1")
        genre = mysql.fetchall()
        print("Most Read Genre: ",genre)

    elif choice == 6:
        break
