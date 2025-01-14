SELECT period as period,
    trim(program_stream) as stream, 
    trim(employer) as employer, 
    split(address, ',')[0] as city, 
    regexp_substr(address, '(\\D\\d\\D \\D\\d\\D)', 1) as postal_code,
    trim(province) as province, 
    regexp_substr(occupation, '(\\d*)(?:-)', 1) as occupation_code,
    regexp_substr(occupation, '(?:-)(.*)', 1) as occupation_name,
    approved_lmia_count as approved_lmias,
    approved_positions as approved_positions
FROM lmia.lmia_applications_raw
WHERE occupation is not null
and address is not null