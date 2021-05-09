def custom_normalize(to_convert, input_range, output_range):
    """
        Parameters:
            to_convert --> number to convert from input range to output range
            input_range --> list of 2 integer of float items
            output_range --> list of 2 integer of float items
    """
    assert len(input_range) == 2, "Input range should be list of 2 items"
    assert len(output_range) == 2, "Output range should be list of 2 items"
    assert type(to_convert) == int or type(to_convert) == float, "Only integer and float is allowed to convert"

    bipolar_ouput_range = False

    for i in input_range + output_range:
        assert type(i) == int or type(i) == float, "Only integers and floats are allowed in range values"
        if i < 0:
            bipolar_ouput_range = True

    if bipolar_ouput_range:
        coefficient = abs((input_range[0] - input_range[1])/(output_range[0] - output_range[1]))

        if to_convert < 0:
            return max(round(to_convert/coefficient-output_range[1], 2), output_range[0])
        return min(round(to_convert/coefficient-output_range[1], 2), output_range[1])
    else:
        coefficient = abs((input_range[0] - input_range[1])/(output_range[0] - output_range[1]))

        if to_convert < 0:
            return max(round(to_convert/coefficient, 2), output_range[0])
        return min(round(to_convert/coefficient, 2), output_range[1])




