import React from "react";

type SearchBarProps = {
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
};

const SearchBar: React.FC<SearchBarProps> = ({ value, onChange, placeholder }) => (
  <div className="flex items-center bg-gray-200 rounded-lg px-4 py-2 w-full max-w-xl">
    <input
      className="bg-transparent outline-none flex-1 text-lg text-gray-800 placeholder-gray-500"
      type="text"
      value={value}
      onChange={e => onChange(e.target.value)}
      placeholder={placeholder || "Enter keywords to search..."}
      aria-label="Search posts"
    />
  </div>
);

export default SearchBar;
