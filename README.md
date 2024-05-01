# Robocorp Level 2 Course - Create RSP Order Robots

Challenge described in the Robocorp Level 2 Automation Developer Course. Rules of the robot are the following:

Before you start with automation, complete the order process manually to see how it works. It is easier to automate a process you are familiar with:

<https://robotsparebinindustries.com/#/robot-order>

Here is a short intro of the process you are going to automate 🎥 video.

<https://youtu.be/0uvexJyJwx>

Ready to build the robot? Know the rules 📚
My dear, without rules there's only chaos. - Star Wars: The Clone Wars: Senate Murders (2010)

The robot should use the orders file (.csv ) and complete all the orders in the file.

<https://robotsparebinindustries.com/orders.csv>

Only the robot is allowed to get the orders file. You may not save the file manually on your computer..

- The robot should save each order HTML receipt as a PDF file
- The robot should save a screenshot of each of the ordered robots.
- The robot should embed the screenshot of the robot to the PDF receipt.
- The robot should create a ZIP archive of the PDF receipts (one zip archive that contains all the PDF files). Store the archive in the output directory.
- The robot should complete all the orders even when there are technical failures with the robot order website.
- The robot should be available in public GitHub repository.
- It should be possible to get the robot from the public GitHub repository and run it without manual setup

All code developed following Hints and Tips from the Robocorp Docs / Courses
