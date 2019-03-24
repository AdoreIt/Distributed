# Lab 2 Two Phase Commit

## Install postrgessql

- `sudo apt update`
- `sudo apt install postgresql postgresql-contrib`

## Change config settings

Ubuntu 18.04:

1. In the "/etc/postgresql/10/main/postgresql.conf" file
(10 - your version of postgressql)<br/>
**change**: "`#max_prepared_transactions = 0`" <br/>
**to**: "`max_prepared_transactions = 10`" (10 - select any number bigger than 0 *to allow prepared thansactions*)

2. In the "/etc/postgresql/10/main/pg_hba.conf" <br/>
   **change** : 

   | local | all | postgres | peer |
   | ----- | --- | -------- | ---- |

   **to**:

   | local | all | postgres | trust |
   | ----- | --- | -------- | ----- |

   *to give postgres user (default) permissions*

3. **restart postgress** : `sudo service postgresql restart`


## Now you can the programm ^_^

