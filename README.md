# AppOptics playground

Sets up dashboard, and some charts in your AppOptics account

## Tests missing

Didn't realized quickly how to mock AppOptics API calls, so tests missing here.

## Usage

```bash
pip3 install -r requirements.txt
chmod u+x submit.py
./submit.py --help
```

To configure charts edit `conf/charts.yaml`

To setup charts:

```
./submit.py <API token> -C
```
