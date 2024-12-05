touch command-task.md
echo "Добавил одну строку текста" > command-task.md
ls
cat command-task.md
echo "Добавил вторую строку текста" >> command-task.md
cat command-task.md
head -n 2 command-task.md
tail -n 1 command-task.md
touch command-task2.md
ls
mkdir new-directory
mv command-task.md new-directory/
cp command-task2.md new-directory/
mv new-directory/command-task2.md new-directory/command-task3.md
ls -l new-directory/
rm command-task3.md
rm command-task.md
mkdir new-directory2
mv new-directory2/ new-directory
mv command-task2.md new-directory/
rm -rf new-directory/

