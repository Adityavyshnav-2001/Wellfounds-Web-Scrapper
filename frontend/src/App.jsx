import React, { useState, useEffect } from "react";
import { Moon, Sun, Search } from "lucide-react";

const App = () => {
	const [keyword, setKeyword] = useState("");
	const [loading, setLoading] = useState(false);
	const [jobs, setJobs] = useState([]);
	const [error, setError] = useState("");
	const [darkMode, setDarkMode] = useState(false);

	useEffect(() => {
		if (darkMode) {
			document.documentElement.classList.add("dark");
		} else {
			document.documentElement.classList.remove("dark");
		}
	}, [darkMode]);

	const handleSearch = async () => {
		setLoading(true);
		setError("");
		setJobs([]);

		try {
			const response = await fetch("http://127.0.0.1:8000/scrape-jobs/", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ keyword }),
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error || "Failed to fetch jobs");
			}

			const data = await response.json();
			setJobs(data.jobs || {});
		} catch (err) {
			setError(err.message || "Something went wrong!");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div
			className={`min-h-screen ${
				darkMode ? "dark bg-gray-900" : "bg-gray-100"
			} transition-colors duration-300 flex items-center justify-center p-4`}
		>
			<div
				className={`max-w-4xl w-full ${
					darkMode ? "bg-gray-800" : "bg-white"
				} shadow-lg rounded-lg p-6`}
			>
				<div className="flex justify-between items-center mb-6">
					<h1
						className={`text-3xl font-bold ${
							darkMode ? "text-white" : "text-gray-800"
						}`}
					>
						Job Scraper
					</h1>
					<button
						onClick={() => setDarkMode(!darkMode)}
						className={`p-2 rounded-full ${
							darkMode
								? "bg-gray-700 text-yellow-300"
								: "bg-gray-200 text-gray-800"
						}`}
					>
						{darkMode ? <Sun size={24} /> : <Moon size={24} />}
					</button>
				</div>
				<div className="flex gap-4 mb-6">
					<div className="relative flex-1">
						<input
							type="text"
							className={`w-full px-4 py-2 pr-10 border rounded-lg focus:outline-none focus:ring-2 ${
								darkMode
									? "bg-gray-700 text-white border-gray-600 focus:ring-blue-500"
									: "bg-white text-gray-800 border-gray-300 focus:ring-blue-500"
							}`}
							placeholder="Enter job keyword (e.g., Software Engineer)"
							value={keyword}
							onChange={(e) => setKeyword(e.target.value)}
						/>
						<Search
							className={`absolute right-3 top-1/2 transform -translate-y-1/2 ${
								darkMode ? "text-gray-400" : "text-gray-500"
							}`}
							size={20}
						/>
					</div>
					<button
						className={`px-6 py-2 rounded-lg text-white flex items-center justify-center transition-colors duration-300 ${
							loading
								? "bg-gray-400"
								: darkMode
								? "bg-blue-600 hover:bg-blue-700"
								: "bg-blue-500 hover:bg-blue-600"
						}`}
						onClick={handleSearch}
						disabled={loading}
					>
						{loading ? (
							<>
								<svg
									className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
								>
									<circle
										className="opacity-25"
										cx="12"
										cy="12"
										r="10"
										stroke="currentColor"
										strokeWidth="4"
									></circle>
									<path
										className="opacity-75"
										fill="currentColor"
										d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
									></path>
								</svg>
								Searching...
							</>
						) : (
							<>
								<Search size={20} className="mr-2" />
								Search
							</>
						)}
					</button>
				</div>
				{error && <p className="text-red-500 text-center mb-6">{error}</p>}
				{Object.keys(jobs).length > 0 && (
					<div
						className={`overflow-hidden rounded-lg ${
							darkMode ? "bg-gray-700" : "bg-white"
						} shadow`}
					>
						<table className="w-full border-collapse">
							<thead>
								<tr
									className={
										darkMode
											? "bg-gray-800 text-gray-200"
											: "bg-gray-50 text-gray-700"
									}
								>
									<th className="p-3 text-left font-semibold">Company</th>
									<th className="p-3 text-left font-semibold">Job Title</th>
								</tr>
							</thead>
							<tbody>
								{Object.entries(jobs).map(([company, jobTitle], index) => (
									<tr
										key={index}
										className={`${
											index % 2 === 0
												? darkMode
													? "bg-gray-800"
													: "bg-gray-50"
												: darkMode
												? "bg-gray-700"
												: "bg-white"
										} transition-colors duration-300`}
									>
										<td
											className={`p-3 ${
												darkMode
													? "text-gray-300 border-gray-600"
													: "text-gray-800 border-gray-200"
											}`}
										>
											{company}
										</td>
										<td
											className={`p-3 ${
												darkMode
													? "text-gray-300 border-gray-600"
													: "text-gray-800 border-gray-200"
											}`}
										>
											{jobTitle}
										</td>
									</tr>
								))}
							</tbody>
						</table>
					</div>
				)}
			</div>
		</div>
	);
};

export default App;
