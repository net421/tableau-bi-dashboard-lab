# Sigma Self-Service BI Notes

Sigma can expose spreadsheet-like exploration while preserving warehouse-backed
governance.

Recommended pattern:

- certified workbook for executive reporting;
- governed source tables;
- reusable controls;
- visible metric dictionary;
- separate sandbox workbook for analyst experimentation;
- scheduled exports only from validated pages.

Do not allow every user to create a different version of OTIF or fill rate.
