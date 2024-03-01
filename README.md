# Farmington Data Tracker

This is a simple project where we keep track of how many wrs, run, games played each player on the database.json has. we run the code every week to post the results on our [discord server](https://discord.gg/dCB96RJDAH). 

## Getting Started

This code is not my version yet, so I will post here the instructions specified by @bluestonex63:


> Ok so the order is:
>
> first you run flags.py to get the updated database
>
> (it takes like 10 mins)
>
> Then you run runsupdater.py
>
> Then pbsupdater.py
>
> Then you have verifierupdater.py
>
> If you want to do a full verifier update you first have to run mods.py
>
> And to actually build the boards you have to use pbslb.py, vlb.py, runslb.py
>
> Oh and for the verifier script there is another script for the over 20k club
>
> Called 1dhareni.py
>
> And you have to manually clean out the output files before running the script
>
> Thats all 🤣
>
> The only important order is to run runsupdater.py before pbsupdater.py for the obsolete runs to be gaming

### Prerequisites

What things you need to install the software and how to install them.


## Running the Code

to run the code we use python IDLE.

**ATTENTION :** As of 2024-02-29, we know this code can randomly haults or just stop wroking mid-way through request, that's why we are always saving the informations.

## Built With

* [python 3](https://www.python.org/) - The language used
* [sr.c API](https://github.com/speedruncomorg/api/tree/master) - the API to get all the data
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Felipe Reis** - *Initial work* - [Github](https://github.com/FelipeReis11011)
* **Rayu_** - *Code Optimizations* - [Deleted Github](https://github.com/Rayu1)
* **Felipe Reis** - *Code De-Optimizations* - [Github](https://github.com/FelipeReis11011)
* **Bluestonex63** - *Maintaining the project from 2022 to 2023* - [Github](https://github.com/Bluestonex63)
* **Felipe Reis** - *Current Developer* - [Github](https://github.com/FelipeReis11011)

See also the list of [contributors](https://github.com/FelipeReis11011/farmington-tracker/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://www.mit.edu/~amini/LICENSE.md) file for details

## Acknowledgments

Huge thanks to Rayu_ who open my mind to optimizations, and to bluestonex63 who kept the project alive while I couldn't.