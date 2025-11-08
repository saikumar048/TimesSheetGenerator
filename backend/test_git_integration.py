import os
import pandas as pd
from utils.git_utils import parse_git

def test_git_integration():
    """
    Test Git integration from utils/git_utils.py
    and confirm that commits are parsed correctly.
    """
    # You can change this path to test another repo
    repo_path = os.getcwd()

    print(f"\n🔍 Testing Git integration for repository: {repo_path}")

    df = parse_git(repo_path)

    if df.empty:
        print("⚠️ No commits found or unable to parse repository.")
        return

    print("\n✅ Git integration successful!")
    print(f"Total Commits Found: {len(df)}\n")

    # Show sample commits
    print(df.head(10).to_string(index=False))

    # Save to CSV
    output_path = os.path.join(repo_path, "git_commits_test_output.csv")
    df.to_csv(output_path, index=False)
    print(f"\n📄 Commit data saved to: {output_path}")

if __name__ == "__main__":
    test_git_integration()
