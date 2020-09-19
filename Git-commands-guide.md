# Git commands
## If your new to project then clone it.(One time)
```sh
$ git clone https://github.com/naaniz/Restaurant-Bot-Automation.git
```
## For regular usage
### To make some changes and push to git remote repo.
### To create a new branch from another branch.
- Switch to specific branch. (check your current branch on vscode editor)
```sh
$ git checkout <branch_name>   
```
- Now create a branch from this current branch as root.
```sh
$ git checkout -b your_patch <branch_name>
```
- First stage your changes by this command
```sh
$ git add . <to stage all files> or git add filename (to stage required file only)
```
- After staging you need to commit the changes once after commit can't undo changes.
```sh
$ git commit -m "feature name u have added"
```
- Now its time to push to the remote repo.
```sh
$ git push
```
- Thats it now your code has been pushed to remote repo.
### But it always won't be smooth as above.
- some times you need to pull before push
```sh
$ git pull
```

>[!WARNING]
>Always check for the current branch your working is right or not and also Never merger pull requests on your own.
