import { ArrowPathIcon } from "@heroicons/react/24/outline";

type FileConvertButtonProps = {
  onConvertClick: () => void;
};

export default function FileConvertButton({
  onConvertClick,
}: FileConvertButtonProps) {
  const handleButtonClick = () => onConvertClick();
  return (
    <button
      type="button"
      onClick={handleButtonClick}
      className="inline-flex items-center gap-x-2 rounded-md bg-blue-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
    >
      Convert
      <ArrowPathIcon className="-mr-0.5 h-5 w-5" aria-hidden="true" />
    </button>
  );
}
