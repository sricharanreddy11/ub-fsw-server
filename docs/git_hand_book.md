# Essential Git Commands Handbook

These are the core commands you'll use daily for synchronizing your work and managing feature branches.

## Forking (Creating your copy on GitHub)

1. **Navigate** to the original repository page: **`https://github.com/Sashi445/ub-fsw-server`**

2. Click the **Fork** button (top right).

3. **Confirm** the action on your account.
   _Result: A new copy exists under your username, e.g., `github.com/YOUR-USERNAME/ub-fsw-server`._

## Cloning (Downloading to your Local Machine)

1. On **your forked repository** page (the one under your username), click the green **Code** button and copy the **HTTPS** URL.

2. Open your **Terminal** or Git Bash.

3. Run the clone command (replace `YOUR-USERNAME` with your actual GitHub username):

> git clone https://github.com/YOUR-USERNAME/ub-fsw-server.git

4. Navigate into the new folder to begin work:

> cd ub-fsw-server

## Synchronizing Changes

> `git pull` (Get Updates)

Fetches and merges changes from the remote repository (e.g., GitHub) into your current local branch. Always run this before starting new work.

> `git push` (Send Updates)

Uploads your local commits to the remote repository. This makes your changes visible to others.

## 2. Managing Branches

Branches allow you to work on new features or fixes without affecting the stable code (`main` or `master`).

> `git checkout -b <branch-name>` (Create and Switch)

This is the shortcut to create a brand **new branch** based on your current location and immediately switch to it.

> `git checkout <branch-name>` (Switch to Existing Branch)

Switches your working directory to an **existing branch**. Make sure your current changes are committed or stashed before running this.

---

## Setting up SSH for Secure Access

Using SSH keys allows you to securely push and pull code without repeatedly entering your username and password.

### Step 1: Generate the Key Pair

Open your terminal and run this command. You can press `Enter` to accept the default file location.

> ssh-keygen -t ed25519 -C "your_email@example.com"

### Step 2: Start the SSH Agent

Run this to ensure the SSH agent is running, which manages your keys.

> eval "$(ssh-agent -s)"

### Step 3: Add Key to Agent

Add your new private key to the agent. You will need to enter your passphrase if you set one.

> ssh-add ~/.ssh/id_ed25519

### Step 4: Copy the Public Key

Display and copy the entire contents of your public key (`.pub` file).

> cat ~/.ssh/id_ed25519.pub

### Step 5: Add Key to GitHub

1. Go to **GitHub Settings** $\rightarrow$ **SSH and GPG keys**.

2. Click **New SSH key** and paste the public key content you copied in Step 4.

3. Give it a descriptive title (e.g., "Workshop Laptop").
