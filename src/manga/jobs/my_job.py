def my_cron_job():
    with open("test.txt", "w") as f:
        f.write("new line\n")
