"use client"
import Link from 'next/link';
import React, { useState, useEffect } from 'react';

function Table() {
    const [people, setPeople] = useState([]);
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetch("http://localhost:8080/users")
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }
            return response.json();
          })
          .then((data) => {
            setMessage(""); // Clear loading message
            setPeople(data); // Set fetched users
          })
          .catch((error) => {
            setMessage("Error fetching data"); // Handle error if fetch fails
            console.error("Error fetching data:", error);
          });
      }, []);

      const handleDelete = (id) => {
        fetch(`http://localhost:8080/userdelete/${id}`, {
            method: 'DELETE',
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Filter out the deleted user from state
            setPeople(people.filter(person => person.id !== id));
            setMessage('User deleted successfully');
        })
        .catch((error) => {
            setMessage('Error deleting user');
            console.error('Error deleting user:', error);
        });
    };


    return (
        <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
            <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                        <th scope="col" className="px-6 py-3">
                            Name
                        </th>
                        <th scope="col" className="px-6 py-3">
                           Email
                        </th>
                        <th scope="col" className="px-6 py-3">
                        Message
                        </th>                        
                        <th scope="col" className="px-6 py-3">
                        Action
                        </th>                        
                        
                    </tr>
                </thead>
                <tbody>
                    {people.map((person, index) => (
                        <tr key={index} className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                            <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                {person.name}
                            </th>
                            <td className="px-6 py-4">
                                {person.email}
                            </td>
                            <td className="px-6 py-4">
                                {person.password}
                            </td>
                           
                            <td className="px-6 py-4 ">
                                <Link href={`/editTopic/${person.id}`} className="font-medium text-blue-600 dark:text-blue-500 hover:underline px-2">Edit</Link>
                                <button onClick={() => handleDelete(person.id)} className="font-medium text-red-600 dark:text-red-500 hover:underline px-2">Delete</button>
                            </td>
                        </tr>
                    ))}
                    {message && (
                        <tr>
                            <td colSpan="5" className="px-6 py-4 text-center text-red-500">{message}</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
}

export default Table;
