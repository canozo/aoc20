read_input = fn (filename) ->
  case File.read(filename) do
    {:ok, contents} ->
      contents
      |> String.replace("\r\n", "\n")
      |> String.split("\n", trim: true)
      |> Enum.map(&(String.to_integer(&1)))
    {:error, :enoent} ->
      IO.puts "Could not find #{filename}"
  end
end

filter_nils = fn (list) ->
  list
  |> Enum.filter(&(&1 != nil))
  |> List.first
end

is_valid = fn (number, preambles) ->
  indexed = Enum.with_index preambles
  enum = for {a, id_a} <- indexed, {b, id_b} <- indexed, id_a != id_b, do: a + b
  Enum.member?(enum, number)
end

v1 = fn (filename, initial) ->
  input = read_input.(filename)
  for {preamble, index} <- Enum.with_index Range.new(initial, length(input) - 1) do
    preambles = Enum.slice(input, index, preamble)
    value = Enum.at(input, preamble)
    if !is_valid.(value, preambles) do
      IO.puts "Invalid XMAS value: #{value}"
      value
    end
  end
end

v2 = fn (filename, corrupted) ->
  input = read_input.(filename)
  range = Range.new(0, length(input))
  for start <- range, limit <- range, start != limit and limit - start > 1 do
    section = Enum.slice(input, start, limit - start)
    sum = Enum.sum(section)
    if sum == corrupted do
      weakness = Enum.min(section) + Enum.max(section)
      IO.puts("Weakness hash found for #{corrupted}: #{weakness}")
      weakness
    end
  end
end

result_part1 = filter_nils.(v1.("example.txt", 5))
result_part2 = filter_nils.(v1.("input.txt", 25))

v2.("example.txt", result_part1)
v2.("input.txt", result_part2)
