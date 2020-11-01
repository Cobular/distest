Contributing
============

Hey! You're here because you want to contribute to the bot, and that's awesome! Here are some notes about contributions:

* Please open an issue for your contribution and tag it with contribution to discuss it. Because of my time constraints, I probably won't have much time to implement new features myself, but if you make a feature and PR it in, I'll be more than happy to spend a bit of time testing it out and  add it to the project. The other thing is to make sure you check the github project to see if there is someone else already working on it who you can help.

* You may need to install the additional requirements from `requirements-dev.txt`. This is as simple as running `pip install -r requirements-dev.txt`. This larger list mostly includes things like black for formatting and sphinx for doc testing.

* If you are adding new test types, please make sure you test them well to make sure they work as intended, and please add a demo of them in use to the `example_tests()` for others to see. When you are done, please open a PR and I'll add it in!

* I use Black for my code formatting, it would be appreciated if you could use it when contributing as well. I will remind you when you make a PR if you don't, it is essential to make sure that diffs aren't cluttered up with silly formatting changes. Additionally, CodeFactor *should* be tracking code quality and doing something with PRs. We will see soon exactly how that will work out.

* To build the docs for testing purposes, cd into the docs folder and run `make testhtml`. This will build to a set of HTML files you can view locally.

* Also, if you just want to propose an idea, create an issue and tag it with enhancement. The library is missing tons of features, so let me know what you want to see, and if I have time I'll see about getting around to addign it. Thank you for your help!

